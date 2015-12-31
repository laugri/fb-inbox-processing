from datetime import datetime


class Message(object):
    def __init__(self, meta_soup, message_text=""):
        self.message = message_text
        self.user = meta_soup.find("span", {"class": "user"}).text
        date = meta_soup.find("span", {"class": "meta"}).text
        self.date = datetime.strptime(date[:-7], "%A, %B %d, %Y at %I:%M%p")

    def __repr__(self):
        return (
        	"Message " +
        	str({
	            "user": self.user,
	            "date": str(self.date),
	        })
        )
