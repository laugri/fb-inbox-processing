class Thread(object):
    """docstring for Thread"""
    def __init__(self, soup):
        self.soup = soup

    def participants(self):
        return self.soup.contents[0].replace('  ', '').replace('\n', '')
