from prettytable import PrettyTable
import sys

from csirtgsdk.constants import COLUMNS, MAX_FIELD_SIZE


class Table(object):

    def __init__(self, data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data

    def write(self, fh=sys.stdout):
        t = PrettyTable(self.cols)

        for o in self.data['feed']['indicators']:
            r = []
            for c in self.cols:
                y = ''
                
                if c == 'indicator':
                    c = 'indicator'

                if c == 'user':
                    try:
                        # json returned by --new and --search
                        y = o['indicator']['user']
                    except:
                        # json returned by --feed
                        y = self.data['feed']['user']
                elif c == 'feed':
                    try:
                        y = o['indicator']['feed']
                    except:
                        y = self.data['feed']['name']
                elif c == 'comments':
                    if o['indicator'].get(c):
                        y = len(o['indicator'].get(c)) or ''
                    else:
                        y = ''
                else:
                    y = o['indicator'].get(c) or ''


                # make sure we do this last
                if isinstance(y, list):
                    y = ','.join(y)
                y = str(y)
                y = (y[:self.max_field_size] + '..') if len(y) > self.max_field_size else y
                r.append(y)
            t.add_row(r)
        fh.write(str(t))
        fh.write("\n")
