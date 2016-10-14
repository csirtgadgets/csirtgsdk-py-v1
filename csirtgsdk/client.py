import sys
import os
import os.path
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import textwrap
import json
import requests
import logging

from csirtgsdk.utils import setup_logging, read_config

from csirtgsdk.feed import Feed
from csirtgsdk.indicator import Indicator
from csirtgsdk.search import Search

from csirtgsdk import VERSION
from csirtgsdk.constants import API_VERSION, TIMEOUT, REMOTE, LIMIT, TOKEN
from csirtgsdk.format import factory as format_factory
import csirtgsdk

from pprint import pprint


class Client(object):

    def __init__(self, remote=REMOTE, token=None, proxy=None, timeout=TIMEOUT, verify_ssl=True):
        
        self.logger = logging.getLogger(__name__)
        self.remote = remote
        self.token = str(token)
        self.proxy = proxy
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.verify_ssl:
            self.logger.debug('TLS Verification is OFF')

        self.session = requests.session()
        self.session.headers["Accept"] = 'application/vnd.csirtg.v{0}+json'.format(str(API_VERSION))
        self.session.headers['User-Agent'] = 'csirtgsdk-python/{0}'.format(VERSION)
        self.session.headers['Authorization'] = 'Token token=' + self.token
        self.session.headers['Content-Type'] = 'application/json'

    def get(self, uri, params={}):
        """
        HTTP GET function

        :param uri: REST endpoint
        :param params: optional HTTP params to pass to the endpoint
        :return: list of results (usually a list of dicts)

        Example:
            ret = cli.get('/search', params={ 'q': 'example.org' })
        """

        self.logger.debug(uri)
        self.logger.debug(params)
        if not uri.startswith(self.remote):
            uri = '{}{}'.format(self.remote, uri)
            self.logger.debug(uri)

        body = self.session.get(uri, params=params, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            self.logger.debug(err)
            try:
                err = json.loads(body.text).get('errors')
            except ValueError as e:
                err = body.text

            self.logger.error(err)
            raise RuntimeWarning(err)

        body = json.loads(body.text)
        return body

    def post(self, uri, data):
        """
        HTTP POST function

        :param uri: REST endpoint to POST to
        :param data: list of dicts to be passed to the endpoint
        :return: list of dicts, usually will be a list of objects or id's

        Example:
            ret = cli.post('/indicators', { 'indicator': 'example.com' })
        """

        if not uri.startswith(self.remote):  # append self.remote if the uri doesn't include it
            uri = '{}/{}'.format(self.remote, uri)
            self.logger.debug(uri)

        data = json.dumps(data)

        body = self.session.post(uri, data=data, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            self.logger.error(err)
            err = body.text

            if body.status_code == 401:
                err = 'unauthorized'
                raise RuntimeError(err)
            elif body.status_code == 404:
                err = 'not found'
                raise RuntimeError(err)
            elif body.status_code == 422:
                err = json.loads(err)['message']
                #err = 'invalid indicator: {}'.format(d['indicator']['indicator'])
                raise RuntimeError(err)
            elif body.status_code >= 500:
                err = 'unknown 500 error, contact administrator'
                raise RuntimeError(err)
            else:
                try:
                    err = json.loads(err).get('message')
                except ValueError as e:
                    err = 'unknown error, contact administrator'

                self.logger.error(err)
                raise RuntimeWarning(err)

        self.logger.debug(body.text)
        body = json.loads(body.text)
        return body

    def submit_bulk(self, indicators, user, feed):
        """
        Submit action against the IndicatorBulk endpoint

        :param indicators: list of Indicator Objects
        :param user: feed username
        :param feed: feed name
        :return: list of Indicator Objects submitted

        from csirtgsdk.client import Client
        from csirtgsdk.indicator import Indicator

        remote = 'https://csirtg.io/api'
        token = ''
        verify_ssl = True

        i = {
            'indicator': 'example.com',
            'feed': 'test',
            'user': 'admin',
            'comment': 'this is a test',
        }

        data = []

        cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)

        for x in range(0, 5):
            data.append(
                Indicator(cli, i)
            )

        ret = cli.submit_bulk(data, 'csirtgadgets', 'test-feed')
        """

        uri = '/users/{0}/feeds/{1}/indicators_bulk'.format(user, feed)

        data = {
            'indicators': [
                {
                    'indicator': i.args.indicator,
                    'feed_id': i.args.feed,
                    'tag_list': i.args.tags,
                    "description": i.args.description,
                    "portlist": i.args.portlist,
                    "protocol": i.args.protocol,
                    'firsttime': i.args.firsttime,
                    'lasttime': i.args.lasttime,
                    'portlist_src': i.args.portlist_src,
                    'comment': {
                        'content': i.args.comment
                    }
                } for i in indicators
            ]
        }
        return self.post(uri, data)


def main():
    parser = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ csirtg --search example.com
            $ csirtg --user csirtgadgets --feeds
            $ csirtg --user csirtgadgets --feed uce-urls
            $ csirtg --user csirtgadgets --new --feed scanners --description 'a feed of port scanners'
            $ csirtg --user csirtgadgets --feed scanners --new --indicator 1.1.1.1 --tags scanner --comment
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
    # actions
    parser.add_argument('-q', '--search', help="search for an indicator")
    parser.add_argument('--feeds', action="store_true", help="show a list of feeds (per user)")
    parser.add_argument('--new', action='store_true', help="create a new feed or indicator")


    # vars
    parser.add_argument('--user', help="specify a user")
    parser.add_argument('--feed', help="specify feed name")
    parser.add_argument('--indicator', dest='indicator', help="specify an indicator [eg: 1.2.3.4, example.com, "
                                                           "http://example.com/1.html")
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


    # Process arguments
    args = parser.parse_args()
    setup_logging(args)

    logger = logging.getLogger(__name__)

    ## TODO -- yconf ?
    options = vars(args)
    o = read_config(args)
    options.update(o)

    verify_ssl = True
    if options.get('no_verify_ssl'):
        verify_ssl = False

    cli = Client(remote=options['remote'], token=options['token'], verify_ssl=verify_ssl)

    if options.get('search'):
        logger.info("Searching for: {0}".format(options.get('search')))
        ret = Search(cli).search(options.get('search'), limit=options['limit'])
        format = format_factory(options['format'])
        format(ret).write()
        logger.info("Done")

    elif options.get('feeds'):
        logger.info("Searching feeds for user: {0}".format(options['user']))
        feeds = Feed(cli).index(options['user'])
        from prettytable import PrettyTable
        cols = ['name', 'description', 'license', 'updated_at']
        t = PrettyTable(cols)
        for f in feeds:
            r = []
            for c in cols:
                y = f['feed'].get(c)
                if c == 'license':
                    y = y['name']
                y = str(y)
                y = (y[:30] + '..') if len(y) > 30 else y
                r.append(y)
            t.add_row(r)
        print(str(t))
        logger.info("Done")

    elif options.get('feed') and options.get('new') and (not options.get('indicator') and not options.get('attachment')):
        if not options.get('user'):
            parser.error('--user is required')

        logger.info("Creating feed {0} for user {1}".format(options['feed'], options['user']))
        feed = Feed(cli).new(options['user'], options['feed'], description=options['description'])

        from prettytable import PrettyTable
        cols = ['name', 'description', 'license', 'updated_at']
        t = PrettyTable(cols)
        r = []
        for c in cols:
            y = feed.get(c)
            if c == 'license':
                y = y['name']
            y = str(y)
            y = (y[:30] + '..') if len(y) > 30 else y
            r.append(y)
        t.add_row(r)

        print(str(t))
        logger.info("Done")

    elif options.get('feed') and not options.get('new'):
        if not options.get('user'):
            parser.error('--user is required')

        logger.info("Fetching feed {0} for user {1}".format(options['feed'], options['user']))
        data = Feed(cli).show(
                options['user'],
                options['feed'],
                limit=options['limit'],
                lasttime=options['lasttime'],
        )

        if data['feed'].get('indicators'):
            format = format_factory(options['format'])
            if options['format'] == 'csv' or options['format'] == 'table':
                print(format(data).write())
            else:
                print(format(data))
        logger.info("Done")

    # submit new indicator
    elif options.get('feed') and (options.get('indicator') or (options.get('attachment') and not options.get('indicator'))) and options.get('new') and options.get('user'):
        try:
            logger.info("Creating indicator in feed {0} for user {1}".format(options['feed'],options['user']))
            ret = Indicator(cli, options).submit()
            logger.info('posted: {0}'.format(ret['indicator']['location']))
            ret = {
                'feed': {
                    'indicators': [ret]
                }
            }
            format = format_factory(options['format'])
            format(ret).write()
            logger.info("Done")

        except RuntimeError as e:
            logger.error(e)

if __name__ == "__main__":
    main()
