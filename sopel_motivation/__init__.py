# coding=utf8
"""sopel-motivation

A Sopel plugin to fetch motivational quotes on command.
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import requests

from sopel import plugin
from sopel.config import ConfigurationError
from sopel.config.types import StaticSection, ValidatedAttribute


class MotivationSection(StaticSection):
    endpoint = ValidatedAttribute('endpoint', default='https://justmotivate.me/api/getQuote')
    """API endpoint returning quotes in JSON format."""

    quote_key = ValidatedAttribute('quote_key', default='text')
    """JSON key containing quote text."""

    author_key = ValidatedAttribute('author_key', default='by')
    """JSON key containing author's name/attribution."""


def setup(bot):
    bot.config.define_section('motivation', MotivationSection)

    if not bot.config.motivation.endpoint:
        raise Exception('Empty API endpoint setting.')


@plugin.commands('motivate', 'mq')
@plugin.output_prefix('[motivation] ')
def motivate_me(bot, trigger):
    """Fetch and display a motivational quote. No arguments."""
    try:
        r = requests.get(bot.config.motivation.endpoint)
        r.raise_for_status()
    except requests.RequestException:
        bot.reply("Couldn't contact the quote service. Please try again later.")
        return plugin.NOLIMIT

    # assume success
    try:
        data = r.json()
        data[bot.config.motivation.quote_key]
        data[bot.config.motivation.author_key]
    except JSONDecodeError:
        # unless decoding JSON fails
        bot.reply("Malformed API response. Try again later.")
        return plugin.NOLIMIT

    # this time for real
    bot.say('"{}" — {}'.format(
        data[bot.config.motivation.quote_key],
        data[bot.config.motivation.author_key]
    ))
