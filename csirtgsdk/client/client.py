import os
import os.path
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import textwrap
import logging

from csirtgsdk.utils import setup_logging, read_config

from csirtgsdk.feed import Feed
from csirtgsdk.indicator import Indicator
from csirtgsdk.search import Search
from csirtgsdk.predict import Predict
from csirtgsdk.constants import TIMEOUT, REMOTE, LIMIT, TOKEN, COLUMNS
from csirtg_indicator.format import FORMATS
from csirtgsdk.client.http import HTTP as Client


def main():
    parser = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ csirtg --search example.com
            $ csirtg --user csirtgadgets --feeds
            $ csirtg --user csirtgadgets --feed uce-urls
            $ csirtg --user csirtgadgets --feed-new scanners --description 'a feed of port scanners'
            $ csirtg --user csirtgadgets --feed scanners --indicator-new 1.1.1.1 --tags scanner --comment
              'this is a port scanner'
            $ csirtg --user csirtgadgets --feed uce-attachments --new --attachment 'fax.zip'
              --description 'file attached in uce email'
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='csirtg'
    )

    parser.add_argument("-v", "--verbose", action="count", help="set verbosity level [default: %(default)s]")
    parser.add_argument('-d', '--debug', action="store_true")

    parser.add_argument('--token', help="specify token", default=TOKEN)
    parser.add_argument('-l', '--limit', help="specify results limit [default: %(default)s]", default=LIMIT)
    parser.add_argument('--remote', help="remote api location [default: %(default)s]", default=REMOTE)
    parser.add_argument('--timeout', help='connection timeout [default: %(default)s]', default=TIMEOUT)
    parser.add_argument('-C', '--config', help="configuration file [default: %(default)s]",
                        default=os.path.expanduser("~/.csirtg.yml"))  # env var

    parser.add_argument('--format', help="specify an output format [default: %(default)s]", default='table')
    parser.add_argument('--columns', help='specify output columns [default %(default)s]', default=','.join(COLUMNS))

    # actions
    parser.add_argument('-q', '--search', help="search for an indicator")
    parser.add_argument('--feeds', action="store_true", help="show a list of feeds (per user)")
    parser.add_argument('--new', action='store_true', help="create a new feed or indicator")

    parser.add_argument('--predict', help="test an indicator against the prediction api")
    parser.add_argument('--predict-stdin', action="store_true")

    # vars
    parser.add_argument('--user', help="specify a user")
    parser.add_argument('--feed', help="specify feed name")
    parser.add_argument('--feed-new', help='help specify a new feed')
    parser.add_argument('--indicator', dest='indicator', help="specify an indicator [eg: 1.2.3.4, example.com, "
                                                           "http://example.com/1.html")
    parser.add_argument('--indicator-new', help='create a new indicator')
    parser.add_argument('--tags', help="specify tags")
    parser.add_argument('--comment', help="enter a comment for the indicator")
    parser.add_argument('--description', help="specify a feed description")

    parser.add_argument('--portlist', help="specify a portlist [eg: 22,23-35,443]")
    parser.add_argument('--protocol', help="specify TCP, UDP or ICMP")

    parser.add_argument('--firsttime', help="timestamp when first seen [eg: 2015-11-23T00:00:00Z]")
    parser.add_argument('--lasttime', help="timestamp when last seen [eg: 2015-11-24T00:00:00Z], treated as 'greater "
                                           "than'")

    parser.add_argument('--attachment', help="specify an attachment [eg: /path/to/file]")
    parser.add_argument('--attachment-name', help="specify the attachment filename")

    parser.add_argument('--no-verify-ssl', help='Turn TLS verification OFF', action="store_true")

    parser.add_argument('--sinkhole', action='store_true')


    # Process arguments
    args = parser.parse_args()
    setup_logging(args)

    logger = logging.getLogger(__name__)

    if args.verbose:
        logger.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    options = vars(args)
    o = read_config(args)
    options.update(o)

    verify_ssl = True
    if options.get('no_verify_ssl'):
        verify_ssl = False

    cli = Client(remote=options['remote'], token=options['token'], verify_ssl=verify_ssl)

    if options.get('sinkhole'):
        import sys
        if not sys.stdin.isatty():
            stdin = sys.stdin.read()
        else:
            logger.error("No data passed via STDIN")
            raise SystemExit

        from csirtgsdk.sinkhole import Sinkhole
        ret = Sinkhole(cli).post(stdin)

        if ret.get('status') == 'unauthorized':
            logger.error('unauthorized')
        else:
            if logger.getEffectiveLevel() == logging.DEBUG:
                print("Predictions: \n")
                for p in ret.get('predictions', []):
                    print("\t%s" % p)

        raise SystemExit

    if options.get('predict') or options.get('predict_stdin'):
        import sys
        if options.get('predict'):
            logger.info("Searching for: {0}".format(options.get('predict')))
            predict = options['predict']
            ret = Predict(cli).get(predict)
            print("Prediction Score: %s - %s" % (ret, predict))
        else:
            import sys
            if not sys.stdin.isatty():
                for predict in sys.stdin.read().split("\n"):
                    if predict == '':
                        continue
                    ret = Predict(cli).get(predict)
                    print("Prediction Score: %s - %s" % (ret, predict))
            else:
                logger.error("No data passed via STDIN")
                raise SystemExit

        raise SystemExit

    if options.get('search'):
        logger.info("Searching for: {0}".format(options.get('search')))
        ret = Search(cli).search(options.get('search'), limit=options['limit'])
        if isinstance(ret, dict):
            ret = [ret]

        print(FORMATS[options.get('format')](data=ret, cols=args.columns.split(',')))
        raise SystemExit

    if options.get('indicator_new') or options.get('attachment'):
        options['indicator'] = options['indicator_new']
        logger.info("Creating indicator in feed {0} for user {1}".format(options['feed'], options['user']))
        ret = Indicator(cli, options).submit()
        logger.info('posted: {0}'.format(ret['location']))

        if isinstance(ret, dict):
            ret = [ret]

        print(FORMATS[options.get('format')](data=ret, cols=args.columns.split(',')))
        raise SystemExit

    if options.get('feeds'):
        logger.info("Searching feeds for user: {0}".format(options['user']))
        f = Feed(cli)
        feeds = f.index(options['user'])
        for l in f.get_lines(feeds):
            print(l)
        raise SystemExit

    if options.get('feed_new'):
        if not options.get('user'):
            parser.error('--user is required')

        if not options.get('description'):
            parser.error('--description is required')

        logger.info("Creating feed {0} for user {1}".format(options['feed_new'], options['user']))
        f = Feed(cli)
        feed = f.new(options['user'], options['feed_new'], description=options['description'])
        for l in f.get_lines(feed):
            print(l)

        raise SystemExit

    if options.get('feed'):
        if not options.get('user'):
            parser.error('--user is required')

        logger.info("Fetching feed {0} for user {1}".format(options['feed'], options['user']))
        data = Feed(cli).show(
                options['user'],
                options['feed'],
                limit=options['limit'],
                lasttime=options['lasttime'],
        )

        if data.get('indicators'):
            print(FORMATS[options.get('format')](data=data['indicators'], cols=args.columns.split(',')))


if __name__ == "__main__":
    main()
