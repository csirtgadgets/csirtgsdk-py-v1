import csv
import sys
import logging

from csirtgsdk.constants import COLUMNS, MAX_FIELD_SIZE


class CSV(object):

    def __init__(self, data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        cols += [u'firsttime', u'created_at', u'itype', u'lasttime', u'id']
        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data
        self.logger = logging.getLogger(__name__)

    def write(self, fh=sys.stdout):
        t = csv.DictWriter(fh, delimiter=',', fieldnames=self.cols)
        t.writeheader()

        try:
            feedname = self.data['feed']['name']
            username = self.data['feed']['user']
        except KeyError:
            try:
                feedname = self.data['feed']['indicators'][0]['indicator']['feed']
                username = self.data['feed']['indicators'][0]['indicator']['user']
            except IndexError:
                self.logger.info("No results to format as csv")
        except Exception as e:
            raise RuntimeWarning(e)

        for _ in self.data['feed']['indicators']:
            o = _['indicator']
            o['feed'] = feedname
            o['user'] = username

            for i in ['license', 'location', 'thing']:
                if i in o: del o[i]

            try:
                o['comments'] = len(o['comments'])
            except:
                o['comments'] = 0

            if o.get('tags'):
                o['tags'] = ','.join(o['tags'])

            t.writerow(o)
