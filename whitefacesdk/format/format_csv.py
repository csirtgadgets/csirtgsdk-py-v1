import csv
import sys

from whitefacesdk.constants import COLUMNS, MAX_FIELD_SIZE


class CSV(object):

    def __init__(self, data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        cols += [u'firsttime', u'created_at', u'itype', u'lasttime', u'id']
        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data

    def write(self, fh=sys.stdout):
        t = csv.DictWriter(fh, delimiter=',', fieldnames=self.cols)
        t.writeheader()

        try:
            feedname = self.data['feed']['name']
            username = self.data['feed']['user']
        except:
            feedname = self.data['feed']['indicators'][0]['indicator']['feed']
            username = self.data['feed']['indicators'][0]['indicator']['user']

        for _ in self.data['feed']['indicators']:
            o = _['indicator']
            o['feed'] = feedname
            o['user'] = username

            for i in ['license', 'location']:
                if i in o: del o[i]

            try:
                o['comments'] = len(o['comments'])
            except:
                o['comments'] = 0

            o['tags'] = ','.join(o['tags'])
            t.writerow(o)
