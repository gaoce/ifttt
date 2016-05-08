# -*- coding: utf-8 -*-
from unittest import TestCase
import time
from datetime import datetime
from ifttt import get_feeds, parse_feed, TimeStamp, update_feeds


class TestRss(TestCase):
    def test_get_feeds_txt(self):
        feeds = get_feeds('./tests/rss.txt')
        self.assertEqual(len(feeds), 2)

    def test_get_feeds_opml(self):
        feeds = get_feeds('./tests/rss.opml')
        self.assertEqual(len(feeds), 1)

    def test_time_stamp(self):
        time_stamp = TimeStamp()

        time_origin = time.localtime(0)
        expired = time_stamp.test_expire(time_origin)
        self.assertTrue(expired, 'Must be expired')

        time_latest = datetime.now().timetuple()
        not_expired = time_stamp.test_expire(time_latest)
        self.assertFalse(not_expired)

    def test_parse_feed(self):
        feed = parse_feed('./tests/rss.xml', TimeStamp(None))
        self.assertEqual(feed[0], u'Post Activity')
        self.assertEqual(len(feed[1]), 2)

    def test_update_feeds(self):
        feeds = update_feeds('./tests/rss.opml', TimeStamp(None))

        output = {u'Post Activity': [
            {'date': '2016-05-03 06:01',
             'desc': u'D1',
             'link': u'https://www.example.org/1',
             'title': u'题目1'},
            {'date': '2016-05-03 06:02',
             'desc': u'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dignissim turpis sed nisi gravida viverra. Nunc finibus varius diam. Mauris mauris velit, varius vel vestibulum in, convallis ut orci. Phasellus varius iaculis dui, sed elementum sapien volutpat ac. Integer vehicula tempus magna, interdum suscipit ipsum semper vel. Quisque elementum ut sem vitae egestas. Proin sodales nulla id urna aliquet, nec sodales lacus feugiat. Donec dignissim pharetra sem ut vestibulum. Suspendisse egestas fauci...',
             'link': u'https://www.example.org/2',
             'title': u'Lorem ipsum dolor si...'}
        ]}
        self.assertDictEqual(feeds, output)




