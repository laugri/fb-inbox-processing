class Thread(object):
    """docstring for Thread"""
    def __init__(self, soup):
        self.soup = soup

    def participants(self):
        return self.soup.contents[0].replace('  ', '').replace('\n', '')

    def messages_meta(self, text_only=False):
        metas = self.soup.find_all('div',
                                   {'class': 'message'},
                                   recursive=False)
        return metas

    def messages_text(self, text_only=False):
        texts = self.soup.find_all('p', recursive=False)
        return texts

    @staticmethod
    def extract_text(soup_list):
        return [elem.text for elem in soup_list]
