from bs4 import BeautifulSoup


# Do some stuff
file_path = 'data/messages.htm'
f = open(file_path, 'r')
html_content = f.read(1000)
soup = BeautifulSoup(html_content)
print(soup)
