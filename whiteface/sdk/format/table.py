from prettytable import PrettyTable
from whiteface.sdk.format import COLUMNS, MAX_FIELD_SIZE

from pprint import pprint
class Table(object):

    def __init__(self, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE, data=[]):
        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data

    def __repr__(self):
        t = PrettyTable(self.cols)
        for o in self.data['feed']['observables']:
            r = []
            for c in self.cols:
                if c == 'observable':
                    c = 'thing'

                y = o['observable'].get(c) or ''
                if c == 'comments':
                    y = len(y)

                # make sure we do this last
                if isinstance(y, list):
                    y = ','.join(y)
                y = str(y)
                y = (y[:self.max_field_size] + '..') if len(y) > self.max_field_size else y
                r.append(y)
            t.add_row(r)
        return str(t)