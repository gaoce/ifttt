# -*- coding: utf-8 -*-
from ifttt.email import email_feeds
from ifttt.feeds import *
import os.path
import logging


home_dir = os.path.expanduser('~')
logging.basicConfig(filename=os.path.join(home_dir, '.ifttt/log'),
                    format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


def main():
    logging.info('Start ifttt session')
    file_path = os.path.join(home_dir, '.ifttt/rss.opml')
    rss_feeds = update_feeds(file_path)
    email_feeds(rss_feeds)
    logging.info('Finish ifttt session')
