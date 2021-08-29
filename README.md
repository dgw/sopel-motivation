# sopel-motivation

A Sopel plugin to fetch motivational quotes on command.

## Commands

- **`.motivate` (alias `.mq`):** Fetch and display a motivational quote.

## Credits

Quotes currently come from [justmotivate.me](https://justmotivate.me), which
does not advertise a public API but its front-end uses a couple of JSON
endpoints that are very simple to consume.

## Configuration

In case the API behavior changes, or `justmotivate.me` goes down/starts
blocking bots, this plugin features configuration values that can be used to
point it elsewhere for a source of quotes:

- `endpoint`: URL to an API endpoint returning quotes in JSON format
- `quote_key`: name of the dictionary key containing the quote text
- `author_key`: name of the dictionary key containing who said/wrote the quote

### JMESPath support

Installing `sopel-motivation` with the `jmespath` extra (e.g. `pip install
sopel-motivation[jmespath]`) enables [JMESPath](https://jmespath.org/) support
in the `quote_key` and `author_key` configuration values, which may be needed
for some alternate APIs that don't return a flat, one-level dictionary. See
the JMESPath documentation for how to construct a query matching your chosen
API's output.
