import sys
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import textwrap
import logging

from csirtgsdk.feed import Feed
from csirtgsdk.indicator import Indicator
from csirtgsdk import search
from csirtgsdk.constants import LIMIT, TOKEN, COLUMNS
from csirtg_indicator.format import FORMATS
from csirtgsdk.sinkhole import Sinkhole

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'


def main():
    parser = ArgumentParser(
        description=textwrap.dedent("""
example usage:
  $ csirtg --search example.com
  $ csirtg --user csirtgadgets --feeds 
  $ csirtg --user csirtgadgets --feed uce-urls
  $ csirtg --user csirtgadgets --feed-new scanners --description 'scanners'
  $ csirtg --user csirtgadgets --feed scanners --indicator-new 1.1.1.1 \
--tags scanner
  $ csirtg --user csirtgadgets --feed uce-attachments --new \
--attachment 'fax.zip' --description 'file attached in uce email'
        """),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg'
    )

    parser.add_argument("-v", "--verbose", action="count",
                        help="set verbosity level [default: %(default)s]")
    parser.add_argument('-d', '--debug', action="store_true")

    parser.add_argument('--token', help="specify token", default=TOKEN)
    parser.add_argument('-l', '--limit', default=LIMIT,
                        help="specify results limit [default: %(default)s]")

    parser.add_argument('--format', default='table',
                        help="specify an output format [default: %(default)s]")
    parser.add_argument('--columns', default=','.join(COLUMNS),
                        help='specify output columns [default %(default)s]')

    # actions
    parser.add_argument('-q', '--search', help="search for an indicator")
    parser.add_argument('--feeds', action="store_true",
                        help="show a list of feeds (per user)")
    parser.add_argument('--new', action='store_true',
                        help="create a new feed or indicator")

    # vars
    parser.add_argument('--user', help="specify a user")
    parser.add_argument('--feed', help="specify feed name")
    parser.add_argument('--feed-new', help='help specify a new feed')
    parser.add_argument('--indicator', dest='indicator',
                        help="specify an indicator [eg: 1.2.3.4, example.com, "
                        "http://example.com/1.html")
    parser.add_argument('--indicator-new', help='create a new indicator')
    parser.add_argument('--tags', help="specify tags")
    parser.add_argument('--comment', help="enter a comment for the indicator")
    parser.add_argument('--description', help="specify a feed description")

    parser.add_argument('--portlist',
                        help="specify a portlist [eg: 22,23-35,443]")
    parser.add_argument('--protocol', help="specify TCP, UDP or ICMP")
    parser.add_argument('--content')
    parser.add_argument('--provider')

    parser.add_argument('--first_at', help="timestamp when first observed")
    parser.add_argument('--last_at', help="timestamp when last observed")

    parser.add_argument('--attachment',
                        help="specify an attachment [eg: /path/to/file]")
    parser.add_argument('--attachment-name',
                        help="specify the attachment filename")

    parser.add_argument('--no-verify-ssl', help='Turn TLS verification OFF',
                        action="store_true")

    parser.add_argument('--sinkhole', action='store_true')

    # Process arguments
    args = parser.parse_args()

    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)

    logger = logging.getLogger(__name__)

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if not TOKEN:
        print('~/.csirtg.yml configuration no longer supported')
        print('Please setup your environment variables:')
        print("")
        print("export CSIRTG_TOKEN=1234..")
        raise SystemExit

    options = vars(args)
    if options.get('sinkhole'):

        if not sys.stdin.isatty():
            stdin = sys.stdin.read()
        else:
            logger.error("No data passed via STDIN")
            raise SystemExit

        ret = Sinkhole().post(stdin)

        if ret.get('status') == 'unauthorized':
            logger.error('unauthorized')
            raise SystemExit

        print(ret)

        raise SystemExit

    if options.get('search'):
        logger.info("Searching for: {0}".format(options.get('search')))
        ret = search(options.get('search'), limit=options['limit'])
        if isinstance(ret, dict):
            ret = [ret]

        for l in FORMATS[options.get('format')](data=ret,
                                             cols=args.columns.split(',')):
            print(l)
        raise SystemExit

    if options.get('indicator_new') or options.get('attachment'):
        options['indicator'] = options['indicator_new']
        logger.info("Creating indicator in feed {0} for user {1}"
                    .format(options['feed'], options['user']))
        try:
            ret = Indicator(options).submit()
        except Exception as e:
            print(e)
            raise SystemExit

        logger.info('posted: {0}'.format(ret['location']))

        if isinstance(ret, dict):
            ret = [ret]

        print(FORMATS[options.get('format')](data=ret,
                                             cols=args.columns.split(',')))
        raise SystemExit

    if options.get('feeds'):
        logger.info("Searching feeds for user: {0}".format(options['user']))
        f = Feed()
        feeds = f.index(options['user'])
        for l in f.get_lines(feeds):
            print(l)
        raise SystemExit

    if options.get('feed_new'):
        if not options.get('user'):
            parser.error('--user is required')

        if not options.get('description'):
            parser.error('--description is required')

        logger.info("Creating feed {0} for user {1}"
                    .format(options['feed_new'], options['user']))
        f = Feed()
        feed = f.new(options['user'], options['feed_new'],
                     description=options['description'])
        for l in f.get_lines(feed):
            print(l)

        raise SystemExit

    if options.get('feed'):
        if not options.get('user'):
            parser.error('--user is required')

        logger.info("Fetching feed {0} for user {1}"
                    .format(options['feed'], options['user']))
        data = Feed().show(
                options['user'],
                options['feed'],
                limit=options['limit'],
                last_at=options['last_at'],
        )

        if data.get('indicators'):
            print(FORMATS[options.get('format')](data=data['indicators'],
                                                 cols=args.columns.split(',')))


if __name__ == "__main__":
    main()
