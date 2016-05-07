# -*- coding: utf-8 -*-
"""Parse configuration file to get all feed subscription, currently only opml
file is supported
"""

import feedparser
import xml.etree.ElementTree as eT
import multiprocessing
from multiprocessing.dummy import Pool
import time
from datetime import datetime
from functools import partial
import logging


class TimeStamp(object):
    """ Get the current time, store it in a obj, and test whether a date is
    too old based on that time.
    """

    def __init__(self, period=24*3600):
        """ Get current time

        :param int period: period of time in second (default to 1 day)
        If period is None, test_expire will always return False

        """
        self._now = time.mktime(datetime.now().timetuple())

        if period is None:
            period = self._now
        self._period = period

    def test_expire(self, date):
        """ Test whether a __date__ is a __period__ of time old

        :param time.struct_time date: date tuple

        :return: True for expired, False for not
        """
        if date is None:
            return True
        else:
            # Convert date to seconds since epoch
            date = time.mktime(date)

        # Test whether date is old
        if self._now - date > self._period:
            return True
        else:
            return False


def get_feeds(file_path):
    """ Process file containing feed list, return the urls as a list.

    Note for now we are not going to validate the urls.

    :param str file_path: path to feed list file
    The file could be a simple list (one url per line) or a opml file (XML),
    we determine the type simply by extension: .txt for the former, .opml for
    the later.

    :return: a list of url strings

    """

    feeds = []
    if file_path.endswith('.txt'):
        with open(file_path) as fi:
            for line in fi:
                line = line.rstrip()
                if line == '':
                    continue
                feeds.append(line)
    elif file_path.endswith('.opml'):
        tree = eT.parse(file_path)
        root = tree.getroot()
        outlines = root.findall('.//outline')

        for outline in outlines:
            feeds.append(outline.get('xmlUrl'))

    return feeds


def parse_feed(feed, time_stamp=TimeStamp()):
    """

    :param feed:
    :param TimeStamp time_stamp:

    :return dict: a dict mapping feed title to a list of new entries
    """
    # Get parsed feed
    fd = feedparser.parse(feed)

    feed_title = fd.feed.title

    logging.info('Parsing ' + feed_title)

    entries = []
    for entry in fd.entries:
        # Get feed published date
        date = entry.get('published_parsed', None)
        if date is None:
            date = entry.get('updated_parsed', None)

        titl = entry.get('title', feed_title)
        link = entry.get('link')
        desc = entry.get('description', u'No description')

        # If feed is published
        if time_stamp.test_expire(date):
            continue

        entries.append({'title': titl, 'link': link, 'desc': desc,
                        'date': time.strftime("%Y-%m-%d %H:%M", date)})
    return feed_title, entries


def update_feeds(file_path, time_stamp=TimeStamp()):
    """ Update feed subscription

    :param str file_path:
    :param TimeStamp time_stamp:

    :return:
    """

    logging.info('Start updating feeds')
    feeds = get_feeds(file_path)

    num_cpu = multiprocessing.cpu_count()

    # Save one core for other stuff
    if num_cpu >= 2:
        num_cpu -= 1

    # Set up a pool to parse the feed
    # Note we are using ThreadPool here, otherwise logging is a bit complicated
    pool = Pool(num_cpu)
    parser = partial(parse_feed, time_stamp=time_stamp)
    feeds_parsed = pool.map(parser, feeds)

    logging.info('Finish updating feeds')
    # TODO: time out
    return dict(feeds_parsed)


__all__ = ['TimeStamp', 'get_feeds', 'parse_feed', 'update_feeds']
