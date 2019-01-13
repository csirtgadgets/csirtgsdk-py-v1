

from csirtgsdk.constants import TOKEN, REMOTE

from csirtgsdk.feed import Feed
from csirtgsdk.indicator import Indicator
from csirtgsdk.search import Search
from csirtgsdk.client.http import HTTP as Client


def feed(f, limit=25):
    """
    Pull a feed
    :param f: feed name (eg: csirtgadgetes/correlated)
    :param limit: return value limit (default 25)
    :return: Feed dict
    """
    if '/' not in f:
        raise ValueError('feed name must be formatted like: '
                         'csirtgadgets/scanners')

    user, f = f.split('/')

    return Feed().show(user, f, limit=limit)


def search(i, limit=25):
    """
    Search for an indicator
    :param i: indicator (eg: example.com, 192.168.1.1..)
    :param limit: result set limit
    :return: list of dicts
    """

    # Search for an indicator
    return Search().search(i, limit=limit)


def indicator_create(f, i):
    """
    Create an indicator in a feed
    :param f: feed name (eg: wes/test)
    :param i: indicator dict (eg: {'indicator': 'example.com', 'tags': ['ssh'],
    'description': 'this is a test'})
    :return: dict of indicator
    """
    if '/' not in f:
        raise ValueError('feed name must be formatted like: '
                         'csirtgadgets/scanners')

    if not i:
        raise ValueError('missing indicator dict')

    u, f = f.split('/')

    i['user'] = u
    i['feed'] = f

    ret = Indicator(i).submit()

    return ret
