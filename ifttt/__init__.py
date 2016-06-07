# -*- coding: utf-8 -*-
from ifttt.email import email_feeds
from ifttt.feeds import *
import os.path
import logging
import argparse


home_dir = os.path.expanduser('~')
logging.basicConfig(filename=os.path.join(home_dir, '.ifttt/log'),
                    format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


def parse_args():
    parser = argparse.ArgumentParser(description='ifttt')
    parser.add_argument('-no-email', action='store_true', default=False,
                        help='Do not send emails [default: False]')

    return parser.parse_args()


def main():
    logging.info('Start ifttt session')
    args = parse_args()

    file_path = os.path.join(home_dir, '.ifttt/rss.opml')
    rss_feeds = update_feeds(file_path)

    # Opt-out email sending
    if not args.no_email:
        email_feeds(rss_feeds)

    logging.info('Finish ifttt session')
