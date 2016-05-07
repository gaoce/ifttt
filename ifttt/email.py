# -*- coding: utf-8 -*-
import yagmail
from jinja2 import Environment, PackageLoader


def email_feeds(feeds, preview_only=False):
    """ Render feed entries using jinja2 template and send the emails out.

    :param dict feeds: dict mapping feed title to new feed entries (which are
    dict themselves
    :param logical preview_only: if True, email will not be sent

    :return: nothing
    """

    # Get yagmail agent
    if preview_only:
        yag = yagmail.SMTP(smtp_skip_login=True)
    else:
        yag = yagmail.SMTP()

    # Load template
    env = Environment(loader=PackageLoader('ifttt', 'templates'))
    template = env.get_template('template.html')

    # Render html for each feed
    for feed_title, entries in feeds.items():
        # Skip if no new entry
        if len(entries) == 0:
            continue

        subject = u'Daily Digest: {} ({})'.format(feed_title, len(entries))

        html = template.render(entries=entries)

        yag.send(subject=subject, contents=['', html.encode('utf-8')],
                 preview_only=preview_only)
