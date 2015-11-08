from bs4 import BeautifulSoup
from models.thread import Thread


file_path = 'data/sample.html'
f = open(file_path, 'r')
raw_html_content = f.read()
soup = BeautifulSoup(raw_html_content, 'html.parser')
body = soup.html.body
contents = body.find('div', {'class': 'contents'}, recursive=False)
user = contents.h1.text
threads = contents.div.find_all('div', {'class': 'thread'}, recursive=False)

for thread_soup in threads:
    thread = Thread(thread_soup)
    print(thread.participants())
