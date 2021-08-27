# coding=utf8
"""sopel-motivation

A Sopel plugin to fetch motivational quotes on command.
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import requests

from sopel import plugin


@plugin.commands('motivate', 'mq')
@plugin.output_prefix('[motivation] ')
def motivate_me(bot, trigger):
    """Fetch and display a motivational quote. No arguments."""
    try:
        r = requests.get('https://justmotivate.me/api/getQuote')
        r.raise_for_status()
    except (requests.RequestException, HTTPError):
        bot.reply("Couldn't contact the quote service. Please try again later.")
        return plugin.NOLIMIT

    # assume success
    try:
        data = r.json()
        data['text']
        data['by']
    except JSONDecodeError:
        # unless decoding JSON fails
        bot.reply("Malformed API response. Try again later.")
        return plugin.NOLIMIT

    # this time for real
    bot.say('"{}" — {}'.format(data['text'], data['by']))
