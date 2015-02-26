#!/usr/bin/env python

import sys
import os
import os.path
from whiteface.sdk.client import Client
import yaml
import logging
import tailer
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import re
from pprint import pprint
import socket

REMOTE = 'https://whiteface.csirtgadgets.com/api'
DEFAULT_FILE = '/var/log/auth.log'
#PATTERN_RE = re.compile('^Invalid user (\S+) from (\S+)$')
PATTERN_RE = r'unknown user for illegal user \S+ from (\S+)'

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # Setup argument parser
    parser = ArgumentParser(description='', formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument('-d', '--debug', dest='debug', action="store_true")

    parser.add_argument('--token', dest='token', help="specify token")
    parser.add_argument('--remote', dest="remote", help="remote api location [default: %(default)s]",
                        default=REMOTE)

    parser.add_argument('-C', '--config', dest="config", help="configuration file [default: %(default)s]",
                        default=os.path.expanduser("~/.wf.yml") )

    parser.add_argument('--file', dest="file", default=DEFAULT_FILE)

    parser.add_argument('--user', dest="user")
    parser.add_argument('--feed', dest="feed")
    parser.add_argument('--comment', dest="comment")

    parser.add_argument('--portlist', dest="portlist", default=22)
    parser.add_argument('--protocol', dest='protocol', default='TCP')
    parser.add_argument('--tags', dest="tags", default="ssh, scanner")

    args = parser.parse_args()

    fmt = '%(asctime)s - %(levelname)s - %(name)s::%(threadName)s - %(message)s'
    loglevel = logging.WARNING

    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(fmt))
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)

    options = vars(args)

    # TODO -- defaults
    if os.path.isfile(args.config):
        f = file(args.config)
        config = yaml.load(f)
        f.close()
        if not config:
            raise Exception("Unable to read " + args.config + " config file")
        for k in config:
            if not options.get(k):
                options[k] = config[k]

        if config.get('remote') and (options['remote'] == REMOTE):
            options['remote'] = config['remote']


    cli = Client(**options)

    for line in tailer.follow(open(args.file)):
        x = re.search(r'unknown user for illegal user \S+ from (\S+)', line)
        if x:
            try:
                socket.inet_aton(x.group(1))
            except socket.error:
                logger.error('invalid address: {0}'.format(x.group(1)))
                pass
            else:
                try:
                    ret = cli.observable_create(options['user'], options['feed'], x.group(1),
                                            portlist=options.get('portlist'), protocol=options.get('protocol'),
                                            tags=options.get('tags'), comment=options['comment'])

                    logger.info('posted: {0}'.ret['observable']['url'])
                except RuntimeError as e:
                    logger.error('post failed: {0}'.format(e))

if __name__ == "__main__":
    sys.exit(main())
