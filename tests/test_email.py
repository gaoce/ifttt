# -*- coding: utf-8 -*-
from unittest import TestCase
from ifttt import email_feeds
from ifttt import update_feeds, TimeStamp


class TestEmail(TestCase):
    def test_email_feed(self):
        feeds = update_feeds('./tests/rss.opml', TimeStamp(None))
        email_feeds(feeds, preview_only=True)
