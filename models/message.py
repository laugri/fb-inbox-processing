from datetime import datetime


class Message(object):
    """docstring for Message"""
    def __init__(self, meta_soup, message_text=""):
        self.message = message_text
        self.user = meta_soup.find("span", {"class": "user"}).text
        date = meta_soup.find("span", {"class": "meta"}).text
        self.date = datetime.strptime(date[:-7], "%A, %B %d, %Y at %I:%M%p")

    def __repr__(self):
        return str({
            "user": self.user,
            "date": str(self.date),
            "message": (self.message[:30] + " ...") if len(self.message) > 30 else self.message
        })
