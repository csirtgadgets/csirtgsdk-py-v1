import os.path

API_VERSION = 0

REMOTE = 'https://whiteface.csirtgadgets.com/api'
REMOTE = os.environ.get('WF_REMOTE', REMOTE)

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

LIMIT = 500
LIMIT = os.environ.get('WF_LIMIT', LIMIT)

TIMEOUT = 300
TIMEOUT = os.environ.get('WF_TIMEOUT', TIMEOUT)

COLUMNS = "user,feed,thing,comments,protocol,portlist,tags,updated_at"
COLUMNS = os.environ.get('WF_COLUMNS', COLUMNS)
COLUMNS = COLUMNS.split(',')

MAX_FIELD_SIZE = 30
MAX_FIELD_SIZE = os.environ.get('WF_MAX_FIELD_SIZE', MAX_FIELD_SIZE)