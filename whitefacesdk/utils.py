import logging
import yaml
import os
from whitefacesdk.constants import REMOTE, LOG_FORMAT


def read_config(args):
    options = {}
    if os.path.isfile(args.config):
        f = file(args.config)
        config = yaml.load(f)
        f.close()
        if not config:
            raise Exception("Unable to read {} config file".format(args.config ))
        for k in config:
            if not options.get(k):
                options[k] = config[k]

        if config.get('remote') and (options['remote'] == REMOTE):
            options['remote'] = config['remote']

    return options


def setup_logging(args):
    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)
