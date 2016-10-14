import re
from csirtgsdk.constants import COLUMNS, MAX_FIELD_SIZE

from pprint import pprint

itype = {
    'ipv4': 'ADDR',
    'url': 'URL',
    'fqdn': 'DOMAIN',
    'md5': 'FILE_HASH',
    'sha1': 'FILE_HASH',
    'sha256': 'FILE_HASH',
}

HEADER = '#' + '\t'.join(['fields', 'indicator', 'indicator_type', 'meta.desc', 'meta.cif_confidence', 'meta.source', 'meta.do_notice'])
SEP = '|'


class Bro(object):
    __name__ = 'bro'

    def __init__(self, data, cols=COLUMNS, max_field_size=MAX_FIELD_SIZE):
        cols += [u'firsttime', u'created_at', u'itype', u'lasttime', u'id']
        self.cols = cols
        self.max_field_size = max_field_size
        self.data = data

    def __repr__(self):
        text = []
        for _ in self.data['feed']['indicators']:
            o = _['indicator']

            for i in ['license', 'location', 'thing', 'attachments']:
                if i in o: del o[i]

            try:
                o['comments'] = len(o['comments'])
            except:
                o['comments'] = 0

            try:
                o['user'] = o['user']
            except:
                o['user'] = self.data['feed']['user']

            try:
                o['feed'] = o['feed']
            except:
                o['feed'] = self.data['feed']['name']

            if o.get('tags'):
                o['tags'] = ','.join(o['tags'])

            r = []
            if o['itype'] is 'url':
                o['indicator'] = re.sub(r'(https?\:\/\/)', '', o['indicator'])

            for c in self.cols:
                y = o.get(c, '-')
                if type(y) is list:
                    y = SEP.join(y)
                y = str(y)
                if c is 'itype':
                    y = 'Intel::{0}'.format(itype[o[c]])
                r.append(y)

            # do_notice
            # https://www.bro.org/bro-exchange-2013/exercises/intel.html
            # https://github.com/csirtgadgets/massive-octo-spice/issues/438
            r.append('T')

            text.append("\t".join(r))

        text = "\n".join(text)

        text = "{0}\n{1}".format(HEADER, text)
        return text
