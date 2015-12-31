from bs4 import BeautifulSoup

def get_file_soup(file_path):
    f = open(file_path, "r")
    raw_html_content = f.read()
    return BeautifulSoup(raw_html_content, "html.parser")

def get_inbox_soup(messages_file_path):
	return get_file_soup(messages_file_path).html.body.find(
		"div",
		{"class": "contents"},
		recursive=False
	)
