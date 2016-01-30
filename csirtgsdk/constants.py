import os.path

API_VERSION = 0

REMOTE = 'https://csirtg.io/api'
REMOTE = os.environ.get('CSIRTG_REMOTE', REMOTE)

TOKEN = os.environ.get('CSIRTG_TOKEN', None)

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

LIMIT = 500
LIMIT = os.environ.get('CSIRTG_LIMIT', LIMIT)

TIMEOUT = 300
TIMEOUT = os.environ.get('CSIRTG_TIMEOUT', TIMEOUT)

COLUMNS = "user,feed,indicator,comments,protocol,portlist,portlist_src,tags,description,updated_at"
COLUMNS = os.environ.get('CSIRTG_COLUMNS', COLUMNS)
COLUMNS = COLUMNS.split(',')

MAX_FIELD_SIZE = 30
MAX_FIELD_SIZE = os.environ.get('CSIRTG_MAX_FIELD_SIZE', MAX_FIELD_SIZE)
