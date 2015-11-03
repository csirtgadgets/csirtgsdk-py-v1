import sys
import os
import os.path
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import textwrap
import json
import requests
import logging

from whitefacesdk.utils import setup_logging, read_config

from whitefacesdk.feed import Feed
from whitefacesdk.observable import Observable
from whitefacesdk.search import Search

from whitefacesdk import VERSION
from whitefacesdk.constants import API_VERSION, TIMEOUT, REMOTE, LIMIT
from whitefacesdk.format import factory as format_factory

from pprint import pprint


class Client(object):

    def __init__(self, remote=REMOTE, token=None, proxy=None, timeout=TIMEOUT, no_verify_ssl=False):
        
        self.logger = logging.getLogger(__name__)
        self.remote = remote
        self.token = str(token)
        self.proxy = proxy
        self.timeout = timeout

        if no_verify_ssl:
            self.verify_ssl = False
        else:
            self.verify_ssl = True
        
        self.session = requests.session()
        self.session.headers["Accept"] = 'application/vnd.wf.v{0}+json'.format(str(API_VERSION))
        self.session.headers['User-Agent'] = 'whiteface-sdk-python/{0}'.format(VERSION)
        self.session.headers['Authorization'] = 'Token token=' + self.token
        self.session.headers['Content-Type'] = 'application/json'

    def get(self, uri, params={}):
        return self._get(uri, params=params)

    def _get(self, uri, params={}):
        self.logger.debug(uri)
        self.logger.debug(params)
        if not uri.startswith(self.remote):
            uri = '{}/{}'.format(self.remote, uri)
            self.logger.debug(uri)

        body = self.session.get(uri, params=params, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            self.logger.debug(err)
            try:
                err = json.loads(body.content).get('message')
            except ValueError as e:
                err = body.content

            self.logger.error(err)
            raise RuntimeWarning(err)

        self.logger.debug(body.content)
        body = json.loads(body.content)
        return body

    def post(self, uri, data):
        return self._post(uri, data)

    def _post(self, uri, data):
        data = json.dumps(data)

        body = self.session.post(uri, data=data, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            self.logger.debug(err)
            err = body.content

            if body.status_code == 401:
                err = 'unauthroized'
                raise RuntimeError(err)
            elif body.status_code == 404:
                err = 'not found'
                raise RuntimeError(err)
            else:
                try:
                    err = json.loads(err).get('message')
                except ValueError as e:
                    err = body.content

                self.logger.error(err)
                raise RuntimeWarning(err)

        self.logger.debug(body.content)
        body = json.loads(body.content)
        return body


def main():
    parser = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ wf --search example.com
            $ wf --user wes --feeds
            $ wf --user wes --feed scanners --new --observable 1.2.3.4 --portlist 22 --tags ssh,scanner
            $ wf --user wes --feed vnc --new
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='wf'
    )

    parser.add_argument("-v", "--verbose", action="count", help="set verbosity level [default: %(default)s]")
    parser.add_argument('-d', '--debug', action="store_true")

    parser.add_argument('--token', help="specify token")
    parser.add_argument('-l', '--limit', help="specify results limit [default: %(default)s]", default=LIMIT)
    parser.add_argument('--remote', help="remote api location [default: %(default)s]", default=REMOTE)
    parser.add_argument('--timeout', help='connection timeout [default: %(default)s]', default=TIMEOUT)
    parser.add_argument('-C', '--config', help="configuration file [default: %(default)s]",
                        default=os.path.expanduser("~/.wf.yml"))  # env var

    parser.add_argument('--format', help="specify an output format [default: %(default)s]", default='table')
    # actions
    parser.add_argument('-q', '--search', help="search for an observable")
    parser.add_argument('--feeds', action="store_true", help="list feeds")
    parser.add_argument('--new', action='store_true', help="create a new feed or observable")


    # vars
    parser.add_argument('--user', help="specify a user")
    parser.add_argument('--feed', help="specify feed name")
    parser.add_argument('--observable', dest='thing', help="specify an observable [eg: 1.2.3.4, evilsite.com, "
                                                           "http://badsite.org/1.html")
    parser.add_argument('--tags', help="specify tags")
    parser.add_argument('--comment', help="specify a comment")
    parser.add_argument('--description', help="specify a feed description")

    parser.add_argument('--portlist', help="specify a portlist [eg: 22,23-35,443]")
    parser.add_argument('--protocol', help="specify TCP, UDP or ICMP")

    parser.add_argument('--firsttime')
    parser.add_argument('--lasttime')


    # Process arguments
    args = parser.parse_args()
    setup_logging(args)

    logger = logging.getLogger(__name__)

    ## TODO -- yconf ?
    options = vars(args)
    o = read_config(args)
    options.update(o)

    cli = Client(remote=options['remote'], token=options['token'])

    if options.get('search'):
        ret = Search(cli).search(options.get('search'), limit=options['limit'])
        format = format_factory(options['format'])
        print(format(ret))

    elif options.get('feeds'):
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

    elif options.get('feed') and options.get('new') and not options.get('observable'):
        if not options.get('user'):
            parser.error('--user is required')

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

    elif options.get('feed') and not options.get('new'):
        if not options.get('user'):
            parser.error('--user is required')

        f = Feed(cli).show(options['user'], options['feed'], limit=options['limit'])
        format = format_factory(options['format'])
        print(format(f.show()))

    elif options.get('feed') and options.get('observable') and options.get('new'):
        try:
            ret = Observable(**options).new()
            logger.info('posted: {0}'.format(ret['observable']['location']))
            ret = {
                'feed': {
                    'observables': [ret]
                }
            }
            format = format_factory(options['format'])
            print(format(ret))

        except RuntimeError as e:
            logger.error(e)

if __name__ == "__main__":
    main()
