import collections
import nltk
import operator

from fbinboxprocessing.models.message import Message


class Thread(object):
    def __init__(self, soup):
        self._soup = soup
        self._messages = None
        self._messages_text = None
        self._messages_meta = None
        self.participants = self._soup.contents[0].replace("  ", "").replace("\n", "").split(", ")

    def __repr__(self):
        return (
            "Thread " +
            str(self.participants)
        )

    def incorporate(self, other_threads):
        """Merges another thread into itself."""
        for thread in other_threads:
            self._soup.append(thread._soup)
        self.clear_private()
        return None

    def clear_private(self):
        self._messages_text = None
        self._messages_meta = None
        self._messages = None

    def detailed_record(self):
        return {
            "participants": self.participants,
            "start_date": self.start_date(),
            "end_date": self.end_date(),
            "messages": self.total_messages(per_user=True),
            "duration": self.duration(),
            "day_attendance": self.attendance("day"),
            "week_attendance": self.attendance("week"),
            "most_frequent_words": self.most_frequent_words(top=10),
        }

    def start_date(self):
        return min(self.messages(), key=lambda message:message.date).date

    def end_date(self):
        return max(self.messages(), key=lambda message:message.date).date

    def duration(self):
        return (self.end_date()-self.start_date()).days

    def messages(self, participant=None):
        """Prefer using the more specific and lightweight
        messages_text and messages_meta method when possible.
        """
        if not self._messages:
            messages = []
            for meta, text in zip(self.messages_meta(), self.messages_text()):
                message = Message(meta, text)
                if (not participant) or (participant == message.user):
                    messages.append(message)
            self._messages = messages
        return self._messages

    def messages_meta(self, text_only=False):
        if not self._messages_meta:
            self._messages_meta = self._soup.find_all(
                "div",
                {"class": "message"},
                recursive=True
            )
        return self._messages_meta

    def messages_text(self, text_only=False):
        if not self._messages_text:
            self._messages_text = self.extract_text(self._soup.find_all("p", recursive=True))
        return self._messages_text

    @staticmethod
    def extract_text(soup_list):
        return [elem.text for elem in soup_list]

    def total_messages(self, per_user=False):
        """Should give results per user and global"""
        messages_meta = self.messages_meta()
        counter = collections.Counter()
        counter["total"] = len(messages_meta)
        if per_user:
            for meta_soup in messages_meta:
                user = Message(meta_soup).user
                counter[user] += 1
        return counter

    def most_frequent_words(self, top=10):
        STOP_WORDS = ["le", "la", "les", "au", "du", "a", "à", "un", "une",
                      "des", "que", "sur", "de", "et", "en"
                      "the", "je", "", "pas", "tu", "c'est", "ça", "en", "?",
                      "mais", "pour", "me", "oui", "!", "ce", "j'ai", "ne", "on"
                      ]
        words = []
        for message_content in self.messages_text():
            for word in message_content.split(" "):
                if word not in STOP_WORDS:
                    words.append(word.lower())
        count = collections.Counter(words).most_common(top)
        return count

    def ngrams(self, n, min_frequency=10):
        """ This function compute the ngrams of the given keywords.
            It returns a list of dict {ngram, frequency}
            ordered from most frequent to least frequent,
            and limited to elements at least 3-frequent.
            Gives retarded results for now.
        """
        ngrams = []
        for message_content in self.messages_text():
            ngrams.extend(nltk.ngrams(message_content.split(), n))

        ngram_frequency_distrib = nltk.FreqDist(ngrams)
        sorted_distrib = sorted(
            ngram_frequency_distrib.items(),
            key=operator.itemgetter(1),
            reverse=True,
        )
        filtered_sorted_distrib = [{"ngram": " ".join(e[0]), "frequency": e[1]}
                                   for e in sorted_distrib if e[1] >= min_frequency]
        return filtered_sorted_distrib

    def attendance(self, span_type):
        counter = collections.Counter()
        for message in self.messages():
            if span_type == "day":
                counter[message.date.hour] += 1
            elif span_type == "week":
                counter[message.date.weekday()] += 1
            else:
                raise ValueError(
                    ("The type '{type}' is not supported."
                     " The method can take either 'day' or 'week'"
                     " as `span_type` argument.").format(type=span_type)
                )
        return counter
