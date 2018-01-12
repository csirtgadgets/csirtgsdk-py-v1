import websocket
import logging
import os
import json
from pprint import pprint
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import textwrap
from csirtgsdk.constants import LOG_FORMAT, TOKEN
REMOTE = 'wss://csirtg.io/firehose'

try:
    import thread
except ImportError:
    import _thread as thread

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

if os.getenv('CSIRTGSDK_HTTP_TRACE' or 1):
    logger.setLevel(logging.DEBUG)

logging.getLogger('websocket').setLevel(logging.WARN)
if os.getenv('CSIRTG_HTTP_WEBSOCKET_TRACE' or 1):
    logging.getLogger('websocket').setLevel(logging.DEBUG)
    websocket.enableTrace(True)


class DefaultHandler(object):
    def __init__(self, remote=REMOTE, token=TOKEN):

        self.handle = websocket.WebSocketApp(
            remote,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            header={'Authorization:Token token=' + token}
        )

    def on_admin_message(self, m):
        if not m.get('type'):
            return False

        if m['type'] in ['ping', 'welcome']:
            return True

        if m['type'] == 'confirm_subscription':
            msg = json.loads(m['identifier'])
            logger.info('subscribed to %s' % msg['channel'])

        return True

    def on_message(self, ws, message):
        logger.debug(message)

        m = json.loads(message)

        if self.on_admin_message(m):
            return

        print(m['message'])

    def on_error(self, ws, error):
        if len(str(error)):
            logger.error(error)

    def on_close(self, ws):
        logger.info(' ### CLOSED ###')

    # https://github.com/tobiasfeistmantl/python-actioncable-zwei/blob/master/actioncable/subscription.py
    # https://github.com/NullVoxPopuli/action_cable_client#the-action-cable-protocol
    def on_open(self, ws):

        data = {
            'command': 'subscribe',
            'identifier': json.dumps({'channel': 'IndicatorsChannel'}),
        }
        ws.send(json.dumps(data))

    def run(self):
        self.handle.on_open = self.on_open
        self.handle.run_forever()


def main():
    class MyHandler(DefaultHandler):
        def on_close(self, ws):
            logger.info("Closed using MyHandler...")


    parser = ArgumentParser(
        description=textwrap.dedent('''\
            example usage:
              $ export CSIRTG_TOKEN=abcdefg1234...
                $ csirtg-firehose -v
            '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg-firehose'
    )

    parser.add_argument("-v", "--verbose", action="count", help="set verbosity level [default: %(default)s]")
    parser.add_argument('-d', '--debug', action="store_true")

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

    h = MyHandler()
    try:
        h.run()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
