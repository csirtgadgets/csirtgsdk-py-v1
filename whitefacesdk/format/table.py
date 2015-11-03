from prettytable import PrettyTable

from whitefacesdk.constants import COLUMNS, MAX_FIELD_SIZE


class Table(object):

    def __init__(self, data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data

    def __repr__(self):
        t = PrettyTable(self.cols)
        try:
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
        except KeyError:
            pass

        return str(t)
