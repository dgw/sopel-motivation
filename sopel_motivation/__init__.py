# coding=utf8
"""sopel-motivation

A Sopel plugin to fetch motivational quotes on command.
"""
from __future__ import unicode_literals, absolute_import, division, print_function

import requests

from sopel import plugin, tools
from sopel.config import ConfigurationError
from sopel.config.types import StaticSection, ValidatedAttribute


try:
    import jmespath
except ImportError:
    jmespath = None


class MotivationSection(StaticSection):
    endpoint = ValidatedAttribute('endpoint', default='https://justmotivate.me/api/getQuote')
    """API endpoint returning quotes in JSON format."""

    quote_key = ValidatedAttribute('quote_key', default='text')
    """JSON key or JMESPath expression containing quote text."""

    author_key = ValidatedAttribute('author_key', default='by')
    """JSON key or JMESPath expression containing author's name/attribution."""


def setup(bot):
    bot.config.define_section('motivation', MotivationSection)

    if not bot.config.motivation.endpoint:
        # can happen if an empty value is left in the config file
        raise ConfigurationError('Empty API endpoint setting.')

    if jmespath:
        bot.memory['motivation'] = tools.SopelMemory()
        try:
            bot.memory['motivation']['quote'] = jmespath.compile(bot.config.motivation.quote_key)
            bot.memory['motivation']['author'] = jmespath.compile(bot.config.motivation.author_key)
        except jmespath.exceptions.JMESPathError:
            del bot.memory['motivation']
            raise ConfigurationError('Invalid JMESPath expression in config')


def shutdown(bot):
    try:
        del bot.memory['motivation']
    except KeyError:
        pass


@plugin.commands('motivate', 'mq')
@plugin.output_prefix('[motivation] ')
def motivate_me(bot, trigger):
    """Fetch and display a motivational quote. No arguments."""
    try:
        r = requests.get(bot.config.motivation.endpoint)
        r.raise_for_status()
    except (requests.RequestException, HTTPError):
        bot.reply("Couldn't contact the quote service. Please try again later.")
        return plugin.NOLIMIT

    # assume request succeeded
    try:
        data = r.json()
    except JSONDecodeError:
        # ...unless decoding JSON fails
        bot.reply("Malformed API response. Try again later.")
        return plugin.NOLIMIT

    if jmespath:
        quote = bot.memory['motivation']['quote'].search(data)
        author = bot.memory['motivation']['author'].search(data)
    else:
        quote = data.get(bot.config.motivation.quote_key)
        author = data.get(bot.config.motivation.author_key)

    if quote is None or author is None:
        bot.reply(
            "Please ask {} to double check my configuration. I can't find the quote."
            .format(bot.config.core.owner)
        )
        return

    # found results; output them
    bot.say('"{}" — {}'.format(quote, author))
