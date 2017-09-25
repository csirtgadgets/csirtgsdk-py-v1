import csv
import sys
import logging

from csirtgsdk.constants import COLUMNS, MAX_FIELD_SIZE


class CSV(object):

    def __init__(self, data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        cols += [u'firsttime', u'created_at', u'itype', u'lasttime', u'id', u'updated_at']
        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data
        self.logger = logging.getLogger(__name__)

    def write(self, fh=sys.stdout):
        t = csv.DictWriter(fh, delimiter=',', fieldnames=self.cols)
        t.writeheader()

        for o in self.data['indicators']:
            for i in ['license', 'location', 'attachments']:
                if i in o: del o[i]

            try:
                o['comments'] = len(o['comments'])
            except:
                o['comments'] = 0

            try:
                o['user'] = o['user']
            except:
                o['user'] = self.data['user']


            try:
                o['feed'] = o['feed']
            except:
                o['feed'] = self.data['name']

            if o.get('tags'):
                o['tags'] = ','.join(o['tags'])

            t.writerow(o)
