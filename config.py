import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = 'Telegram'
BOT_IDENTITY = {
    'token': '5000899571:AAH4cS87dlO9BXCXoaxgEFYhR2ku9fwI1TU',
}
BOT_PREFIX = '/'
BOT_ADMINS = (208907614,)


BOT_DATA_DIR = r'/home/dake/opera/errbot/data'
BOT_EXTRA_PLUGIN_DIR = r'/home/dake/opera/errbot/plugins'

BOT_LOG_FILE = r'/home/dake/opera/errbot/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG
