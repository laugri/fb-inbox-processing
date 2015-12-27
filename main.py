from bs4 import BeautifulSoup

from models.inbox import Inbox
from models.thread import Thread
import pprint as pp


def get_soup(file_path):
    print("opening file...")
    f = open(file_path, "r")
    raw_html_content = f.read()
    return BeautifulSoup(raw_html_content, "html.parser")

# file_path = "data/messages.htm"
file_path = "data/sample.html"
soup = get_soup(file_path)
print("getting the soup...")
inbox_soup = soup.html.body.find("div", {"class": "contents"}, recursive=False)

inbox = Inbox(inbox_soup)
pp.pprint(inbox.detailed_threads())
