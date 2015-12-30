import unittest

from fbinboxprocessing.models.inbox import Inbox
from fbinboxprocessing.models.thread import Thread
from fbinboxprocessing.tests import INBOX_SOUP


class TestInboxMethods(unittest.TestCase):

    def test_stuff(self):
        inbox = Inbox(INBOX_SOUP)
        self.assertTrue(True)
