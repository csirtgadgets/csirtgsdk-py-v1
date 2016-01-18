import json
import sys

from csirtgsdk.constants import COLUMNS, MAX_FIELD_SIZE


class JSON(object):

    def __init__(self, data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        cols += [u'firsttime', u'created_at', u'itype', u'lasttime', u'id']
        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data

    def write(self, fh=sys.stdout):        
        fh.write(json.dumps(self.data['feed']))
        fh.write("\n")
