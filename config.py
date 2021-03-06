# docker setup https://version.helsinki.fi/tike-errbot/docker-errbot/-/blob/master/config.py
#
import os
from os.path import join, dirname
from dotenv import load_dotenv
import logging

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# privacy в настройках botfather нужно отключить для групп
BACKEND = 'TelegramCustom'
BOT_IDENTITY = {
    'token': os.environ.get('BOT_TOKEN'),
}
BOT_PREFIX = '/'
BOT_ADMINS = (910701929,)
# перед использование добавить id групп
CHATROOM_PRESENCE = ()

# BOT_DATA_DIR = os.environ.get('BOT_DATA_DIR', '/home/arman/Desktop/work/errbot/data')
# BOT_EXTRA_PLUGIN_DIR = os.environ.get('BOT_EXTRA_PLUGIN_DIR', '/home/arman/Desktop/work/errbot/plugins')

# # BOT_EXTRA_BACKEND_DIR = os.environ.get('BOT_EXTRA_BACKEND_DIR', '/srv/errbackends')

# BOT_LOG_FILE = os.environ.get('BOT_LOG_FILE', '/home/arman/Desktop/work/errbot/errbot.log')
# BOT_LOG_LEVEL = logging.getLevelName(os.environ.get('BOT_LOG_LEVEL', 'DEBUG'))


# BOT_DATA_DIR = r'/home/arman/Desktop/work/errbot/data'
BOT_DATA_DIR = os.environ.get('BOT_DATA_DIR', '/home/arman/Desktop/work/errbot/data')
BOT_EXTRA_PLUGIN_DIR = os.environ.get('BOT_EXTRA_PLUGIN_DIR', '/home/arman/Desktop/work/errbot/plugins')
BOT_EXTRA_BACKEND_DIR = os.environ.get('BOT_EXTRA_BACKEND_DIR', '/home/arman/Desktop/work/errbot/errbackends')
BOT_LOG_FILE = os.environ.get('BOT_LOG_FILE', '/home/arman/Desktop/work/errbot/errbot.log')
BOT_EXTRA_STORAGE_PLUGINS_DIR = os.environ.get('BOT_EXTRA_STORAGE_PLUGINS_DIR', '/home/arman/Desktop/work/errbot/errstorages')
STORAGE = 'SQL'
STORAGE_CONFIG = {
   'data_url': os.environ.get('PSQL_URL', 'postgresql://admin2:admin@localhost:5432/errbotdb')
   }

BOT_LOG_LEVEL = logging.INFO
BOT_ASYNC = True

MONGO_COMMERCIAL_URI = os.environ.get('MONGO_COMMERCIAL_URI')
MONGO_COMMERCIAL_DB_GROUP = os.environ.get('MONGO_COMMERCIAL_DB_GROUP')
MONGO_OPERA_GUIDE_URI = os.environ.get('MONGO_OPERA_GUIDE_URI', 'mongodb://svc_ob_mongo:pq6EQgtnfZveY5am@rc1a-qa7f4jzfobrcaa1s.mdb.yandexcloud.net:27018/OperaGuide?connectTimeoutMS=10000&authSource=OperaGuide&authMechanism=SCRAM-SHA-256')
MONGO_OPERA_GUIDE_DB_GROUP = os.environ.get('MONGO_OPERA_GUIDE_DB_GROUP', 'OperaGuide')
BUDIBASE_REDIS_PASS = os.environ.get('BUDIBASE_REDIS_PASS', 'budibase')
BUDIBASE_COUCHDB_USERNAME = os.environ.get('BUDIBASE_COUCHDB_USERNAME', 'budibase')
BUDIBASE_COUCHDB_PASSWORD = os.environ.get('BUDIBASE_COUCHDB_PASSWORD', 'budibase')
