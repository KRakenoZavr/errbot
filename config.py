# docker setup https://version.helsinki.fi/tike-errbot/docker-errbot/-/blob/master/config.py
#
import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging

# privacy в настройках botfather нужно отключить для групп
BACKEND = 'Telegram'
BOT_IDENTITY = {
    'token': '5000899571:AAH4cS87dlO9BXCXoaxgEFYhR2ku9fwI1TU',
}
BOT_PREFIX = '/'
BOT_ADMINS = (208907614,)
# перед использование добавить id групп
CHATROOM_PRESENCE = ()

# BOT_DATA_DIR = os.environ.get('BOT_DATA_DIR', '/home/dake/opera/errbot/data')
# BOT_EXTRA_PLUGIN_DIR = os.environ.get('BOT_EXTRA_PLUGIN_DIR', '/home/dake/opera/errbot/plugins')

# # BOT_EXTRA_BACKEND_DIR = os.environ.get('BOT_EXTRA_BACKEND_DIR', '/srv/errbackends')

# BOT_LOG_FILE = os.environ.get('BOT_LOG_FILE', '/home/dake/opera/errbot/errbot.log')
# BOT_LOG_LEVEL = logging.getLevelName(os.environ.get('BOT_LOG_LEVEL', 'DEBUG'))


BOT_DATA_DIR = r'/home/dake/opera/errbot/data'
BOT_EXTRA_PLUGIN_DIR = r'/home/dake/opera/errbot/plugins'

BOT_LOG_FILE = r'/home/dake/opera/errbot/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG
# BOT_ASYNC = True

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_COMMERCIAL_URI = os.environ.get('MONGO_COMMERCIAL_URI')
MONGO_COMMERCIAL_DB_GROUP = os.environ.get('MONGO_COMMERCIAL_DB_GROUP')