# -*- coding: utf-8 -*-
from ifttt.email import email_feeds
from ifttt.feeds import *
import os.path


def main():
    file_path = os.path.join(os.path.expanduser('~'), '.ifttt/rss.opml')
    rss_feeds = update_feeds(file_path)
    email_feeds(rss_feeds)
