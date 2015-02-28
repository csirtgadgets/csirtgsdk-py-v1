import unittest
from whiteface.sdk.feed import Feed


class TestFeed(unittest.TestCase):

    def setUp(self):
        self.feed = Feed(user='wes', name='testfeed')

    def test_user(self):
        self.assertEqual(self.feed.user, 'wes', 'user-mismatch')

    def test_feed(self):
        self.assertEqual(self.feed.name, 'testfeed')


if __name__ == '__main__':
    unittest.main()
