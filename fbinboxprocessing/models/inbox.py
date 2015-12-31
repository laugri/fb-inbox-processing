from fbinboxprocessing.models.thread import Thread


class Inbox(object):
    """Represents a user's Inbox, helps managing its threads."""
    def __init__(self, soup):
        self._soup = soup
        self.user = soup.h1.text
        self.threads = [
            Thread(thread_soup)
            for thread_soup
            in soup.find_all("div", {"class": "thread"}, recursive=True)
        ]

    def find_threads(self, participants, strict=True):
        participants.append(self.user)
        looked_up = set(participants)
        if strict:
            matches = [thread for thread in self.threads if set(thread.participants) == looked_up]
        else:
            matches = [thread for thread in self.threads if looked_up.issubset(set(thread.participants))]
        return matches


    def detailed_threads(self):
        # Needs some refactor
        threads = {}
        for thread in self.threads:
            if thread.participants in threads:
                threads[thread.participants]["messages"] += thread.total_messages()["total"]

                for key, value in thread.attendance("day").items():
                    threads[thread.participants]["day_attendance"][key] += value

                for key, value in thread.attendance("week").items():
                    threads[thread.participants]["week_attendance"][key] += value

                threads[thread.participants]["start_date"] = min(
                    thread.start_date(),
                    threads[thread.participants]["start_date"]
                )

                threads[thread.participants]["end_date"] = max(
                    thread.end_date(),
                    threads[thread.participants]["end_date"]
                )

                threads[thread.participants]["duration"] = (
                    threads[thread.participants]["end_date"] -
                    threads[thread.participants]["start_date"]
                    ).days
            else:
                threads[thread.participants] = {
                    "participants": thread.participants,
                    "start_date": thread.start_date(),
                    "end_date": thread.end_date(),
                    "messages": thread.total_messages()["total"],
                    "duration": thread.duration(),
                    "day_attendance": thread.attendance("day"),
                    "week_attendance": thread.attendance("week"),
                }
        return sorted(
            threads.values(),
            key=lambda k: k["messages"],
            reverse=True
        )
