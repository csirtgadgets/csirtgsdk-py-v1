import csv
import sys

from whitefacesdk.constants import COLUMNS, MAX_FIELD_SIZE


class CSV(object):

    def __init__(self, data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        cols += [u'firsttime', u'created_at', u'otype', u'lasttime', u'id']
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
            feedname = self.data['feed']['observables'][0]['observable']['feed']
            username = self.data['feed']['observables'][0]['observable']['user']

        for _ in self.data['feed']['observables']:
            o = _['observable']
            o['feed'] = feedname
            o['user'] = username

            #print o
            for i in ['description', 'license', 'location']:
                if i in o: del o[i]

            try:
                o['comments'] = len(o['comments'])
            except:
                o['comments'] = 0

            o['tags'] = ','.join(o['tags'])
            t.writerow(o)
