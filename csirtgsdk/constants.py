import os.path

from ._version import get_versions
VERSION = get_versions()['version']
del get_versions

API_VERSION = os.getenv('CSIRTG_API_VERSION', '2')

REMOTE = 'https://be.csirtg.io'
REMOTE = os.getenv('CSIRTG_REMOTE', REMOTE)

TOKEN = os.getenv('CSIRTG_TOKEN', None)

LIMIT = 25
LIMIT = os.getenv('CSIRTG_LIMIT', LIMIT)

TIMEOUT = 30
TIMEOUT = os.getenv('CSIRTG_TIMEOUT', TIMEOUT)

COLUMNS = "user,feed,indicator,last_at,first_at,count,tags,description,cc,rdata"
COLUMNS = os.getenv('CSIRTG_COLUMNS', COLUMNS)
COLUMNS = COLUMNS.split(',')

MAX_FIELD_SIZE = 30
MAX_FIELD_SIZE = os.getenv('CSIRTG_MAX_FIELD_SIZE', MAX_FIELD_SIZE)

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'
