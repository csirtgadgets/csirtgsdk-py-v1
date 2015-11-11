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


class Map(dict):
    """
    http://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
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