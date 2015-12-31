from bs4 import BeautifulSoup
import os

import fbinboxprocessing.utilities as utilities

DIRECTORY_PATH = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FILE_PATH = os.path.join(DIRECTORY_PATH, "sample.html")
INBOX_SOUP = utilities.get_inbox_soup(SAMPLE_FILE_PATH)
