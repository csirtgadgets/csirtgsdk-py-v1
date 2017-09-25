import os.path
import sys

API_VERSION = os.getenv('CSIRTG_API_VERSION', '1')

REMOTE = 'https://csirtg.io/api'
REMOTE = os.getenv('CSIRTG_REMOTE', REMOTE)

TOKEN = os.getenv('CSIRTG_TOKEN', None)

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

LIMIT = 500
LIMIT = os.getenv('CSIRTG_LIMIT', LIMIT)

TIMEOUT = 300
TIMEOUT = os.getenv('CSIRTG_TIMEOUT', TIMEOUT)

COLUMNS = "user,feed,indicator,firsttime,lasttime,count,comments,protocol,portlist,tags,description,cc,asn,asn_desc"
COLUMNS = os.getenv('CSIRTG_COLUMNS', COLUMNS)
COLUMNS = COLUMNS.split(',')

MAX_FIELD_SIZE = 30
MAX_FIELD_SIZE = os.getenv('CSIRTG_MAX_FIELD_SIZE', MAX_FIELD_SIZE)

PYVERSION = 2
if sys.version_info > (3,):
    PYVERSION = 3
