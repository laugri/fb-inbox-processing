import unittest

from fbinboxprocessing.models.inbox import Inbox
from fbinboxprocessing.tests import INBOX_SOUP


class TestInboxMethods(unittest.TestCase):

    def test_inbox_find_threads_strict(self):
        inbox = Inbox(INBOX_SOUP)
        sought_user = "John Smith"
        for thread in inbox.find_threads([sought_user]):
            self.assertEqual(
                set(thread.participants),
                set([sought_user, inbox.user])
            )

    def test_inbox_find_threads_not_strict(self):
        inbox = Inbox(INBOX_SOUP)
        sought_user = "John Smith"
        for thread in inbox.find_threads([sought_user], strict=False):
            self.assertTrue(
                set([sought_user, inbox.user]).issubset(set(thread.participants))
            )

    def test_inbox_detailed_threads(self):
        pass