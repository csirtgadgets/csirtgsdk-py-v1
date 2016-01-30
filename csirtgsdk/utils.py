import logging
import yaml
import os
import sys
from csirtgsdk.constants import REMOTE, LOG_FORMAT, TOKEN
from io import open

def read_config(args):
    """
    Reads in an ArgParse objet with args.confg as the YAML style config path

    :param args: ArgParse object
    :return: dict of options based on ArgParse and the YAML config
    """
    options = {}
    if os.path.isfile(args.config):
        f = open(args.config, 'rt')
        config = yaml.load(f)
        f.close()
        if not config:
            raise Exception("Unable to read {} config file".format(args.config))
        for k in config:
            if not options.get(k):
                options[k] = config[k]

        if config.get('remote') and (options['remote'] == REMOTE):
            options['remote'] = config['remote']

        if args.token:
            options['token'] = args.token

    else:
        raise Exception("Unable to read {} config file".format(args.config))

    return options


def setup_logging(args):
    """
    Sets up basic logging

    :param args: ArgParse arguments
    :return: nothing. sets logger up globally
    """
    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)


class Map(dict):
    """


    Example:
        m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])

    Reference:
        http://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        if (sys.version_info < (3, 0)):
            for arg in args:
                if isinstance(arg, dict):
                    for k, v in arg.iteritems():
                        self[k] = v

            if kwargs:
                for k, v in kwargs.iteritems():
                    self[k] = v
        else:
            for arg in args:
                if isinstance(arg, dict):
                    for k, v in arg.items():
                        self[k] = v

            if kwargs:
                for k, v in kwargs.items():
                    self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]
