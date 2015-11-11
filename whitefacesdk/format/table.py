from prettytable import PrettyTable
import sys

from whitefacesdk.constants import COLUMNS, MAX_FIELD_SIZE


class Table(object):

    def __init__(self, data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data

    def write(self, fh=sys.stdout):
        t = PrettyTable(self.cols)
        for o in self.data['feed']['observables']:
            r = []

            for c in self.cols:
                if c == 'observable':
                    c = 'thing'

                if c == 'user':
                    y = self.data['feed']['user']
                elif c == 'feed':
                    y = self.data['feed']['name']
                elif c == 'comments':
                    try:
                        # only show 1st comment
                        y = o['observable'].get(c)[0]['comment']['comment']
                    except:
                        y = ''
                else:
                    y = o['observable'].get(c) or ''


                # make sure we do this last
                if isinstance(y, list):
                    y = ','.join(y)
                y = str(y)
                y = (y[:self.max_field_size] + '..') if len(y) > self.max_field_size else y
                r.append(y)
            t.add_row(r)
        fh.write(str(t))
        fh.write("\n")
