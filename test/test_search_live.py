import pytest
import os
from pprint import pprint
from csirtgsdk.indicator import Indicator
from csirtgsdk.feed import Feed
from csirtgsdk.client import Client
from csirtgsdk.search import Search

CI_BUILD = os.environ.get('CI_BUILD', False)
TOKEN = os.environ.get('CSIRTG_TOKEN', None)
USER = os.environ.get('CSIRTG_USER', 'wes')
REMOTE = os.environ.get('CSIRTG_REMOTE', 'https://csirtg.io/api')
FEED = os.environ.get('CSIRTG_FEED', 'CI_SEARCH_TEST')

liveonly = pytest.mark.skipif(CI_BUILD is False, reason="CI_BUILD env var not set")


@pytest.fixture
def client():
    return Client(
        token=TOKEN,
        remote=REMOTE
    )


@liveonly
def test_indicator_search_fqdn(client):

    INDICATOR = 'example.com'

    # create feed and test created feed
    f = Feed(client).new(USER, FEED, description='build search test feed')
    assert f['created_at']

    # create test and submit test indicator
    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'indicator': INDICATOR,
        'comment': 'this is a test comment'
    })
    r = i.submit()

    # test creating the indicator
    assert r['indicator']['indicator'] == INDICATOR
    assert r['indicator']['itype'] == 'fqdn'
    assert r['indicator']['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r['feed']['indicators']:
        if record['indicator']['feed'] == 'live-test-feed':
            assert record['indicator']['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_search_ipv4(client):

    INDICATOR = '1.1.1.1'

    # create feed and test created feed
    f = Feed(client).new(USER, FEED, description='build search test feed')
    assert f['created_at']

    # create test and submit test indicator
    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'indicator': INDICATOR,
        'comment': 'this is a test comment'
    })
    r = i.submit()

    # test creating the indicator
    assert r['indicator']['indicator'] == INDICATOR
    assert r['indicator']['itype'] == 'ipv4'
    assert r['indicator']['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r['feed']['indicators']:
        if record['indicator']['feed'] == 'live-test-feed':
            assert record['indicator']['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_search_ipv6(client):

    INDICATOR = '2001:4860:4860::8888'

    # create feed and test created feed
    f = Feed(client).new(USER, FEED, description='build search test feed')
    assert f['created_at']

    # create test and submit test indicator
    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'indicator': INDICATOR,
        'comment': 'this is a test comment'
    })
    r = i.submit()

    # test creating the indicator
    assert r['indicator']['indicator'] == INDICATOR
    assert r['indicator']['itype'] == 'ipv6'
    assert r['indicator']['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r['feed']['indicators']:
        if record['indicator']['feed'] == 'live-test-feed':
            assert record['indicator']['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_search_email(client):

    INDICATOR = 'johndoe@example.com'

    # create feed and test created feed
    f = Feed(client).new(USER, FEED, description='build search test feed')
    assert f['created_at']

    # create test and submit test indicator
    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'indicator': INDICATOR,
        'comment': 'this is a test comment'
    })
    r = i.submit()

    # test creating the indicator
    assert r['indicator']['indicator'] == INDICATOR
    assert r['indicator']['itype'] == 'email'
    assert r['indicator']['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r['feed']['indicators']:
        if record['indicator']['feed'] == 'live-test-feed':
            assert record['indicator']['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_search_url(client):

    INDICATOR = 'http://www.example.com/test/index.html'

    # create feed and test created feed
    f = Feed(client).new(USER, FEED, description='build search test feed')
    assert f['created_at']

    # create test and submit test indicator
    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'indicator': INDICATOR,
        'comment': 'this is a test comment'
    })
    r = i.submit()

    # test creating the indicator
    assert r['indicator']['indicator'] == INDICATOR
    assert r['indicator']['itype'] == 'uri'
    assert r['indicator']['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r['feed']['indicators']:
        if record['indicator']['feed'] == 'live-test-feed':
            assert record['indicator']['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200
