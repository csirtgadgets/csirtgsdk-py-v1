import logging
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import textwrap
from csirtgsdk.constants import LOG_FORMAT
import json
from pprint import pprint
from datetime import datetime
from csirtgsdk.indicator import Indicator
import pickle
import os

from csirtgsdk.client.http import HTTP as Client
from csirtgsdk.firehose import DefaultHandler as FirehoseHandler

REMOTE = 'wss://csirtg.io/firehose'
USER = os.getenv('CSIRTG_USER')
FEED = os.getenv('CSIRTG_FEED')

TRIGGER = os.getenv('CSIRTG_CORRELATION_TRIGGER', '2')
TRIGGER = int(TRIGGER)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


def main():
    class CorrelationHandler(FirehoseHandler):
        context = {}
        today = datetime.today().strftime('%Y-%m-%d')
        trigger = TRIGGER
        cli = Client()

        def on_message(self, ws, message):
            m = json.loads(message)

            if self.on_admin_message(m):
                return

            m = json.loads(m['message'])

            today = datetime.today().strftime('%Y-%m-%d')
            if self.today != today:
                self.context = {}

            if m['indicator'] not in self.context:
               self.context[m['indicator']] = {}
               self.context[m['indicator']]['providers'] = set()
               self.context[m['indicator']]['tags'] = set()
               self.context[m['indicator']]['firsttime'] = m.get('firsttime', datetime.today())

            self.context[m['indicator']]['providers'].add(m['provider'])

            for t in m['tags'].split(','):
               self.context[m['indicator']]['tags'].add(t)

            if len(self.context[m['indicator']]['providers']) >= TRIGGER:
                h = {
                    'description': 'correlated',
                    'tags': ','.join(list(self.context[m['indicator']]['tags'])),
                    'indicator': m['indicator'],
                    'feed': FEED,
                    'user': USER,
                    'firsttime': self.context[m['indicator']]['firsttime']
                }
                ret = Indicator(self.cli, h).submit()
                logger.info('posted: {0}'.format(ret['location']))
                pprint(h)
                pprint(self.context)
                pprint("\n")

    parser = ArgumentParser(
        description=textwrap.dedent('''\
            example usage:
              $ export CSIRTG_TOKEN=abcdefg1234...
                $ csirtg-firehose -v
            '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-firehose'
    )

    parser.add_argument("-v", "--verbose", action="count", help="set verbosity level to INFO")
    parser.add_argument('-d', '--debug', action="store_true")
    parser.add_argument('-r', '--reconnect', action="store_true", help="auto reconnect if connection closes...",
                        default=False)
    parser.add_argument('-s', '--save', help='save results between restarts', action="store_true")
    parser.add_argument('--user', help='user to submit results to [default %(default)s]', default=USER)
    parser.add_argument('--feed', help='feed to submit to [default %(default)s]', default=FEED)

    args = parser.parse_args()

    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    logger.setLevel(loglevel)

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)

    h = CorrelationHandler()

    if os.path.exists('correlator.pickle'):
        with open('correlator.pickle', 'rb') as handle:
            h.context = pickle.load(handle)

    while True:
        h.run()

        # if we closed and it wasn't an error
        if not h.error:
            break

        # if we didn't set the re-connect flag
        if not args.reconnect:
            break

        # we set the re-connect and it was an error, clear the error and re-connect.
        h.error = False

        logger.info('re-connecting..')

    if args.save:
        with open('correlator.pickle', 'wb') as handle:
            pickle.dump(h.context, handle, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
