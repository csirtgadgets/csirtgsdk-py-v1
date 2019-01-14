import pytest
import os
from pprint import pprint
from time import sleep
from csirtgsdk.indicator import Indicator
from csirtgsdk.feed import Feed
from csirtgsdk.client.http import HTTP as Client
from csirtgsdk.search import Search

CI_BUILD = os.environ.get('CI_BUILD', False)
TOKEN = os.environ.get('CSIRTG_TOKEN', None)
USER = os.environ.get('CSIRTG_USER', 'wes')
REMOTE = os.environ.get('CSIRTG_REMOTE', 'https://csirtg.io/api')
FEED = os.environ.get('CSIRTG_TEST_FEED', 'ci_search_test')

liveonly = pytest.mark.skipif(CI_BUILD is False, reason="CI_BUILD env var not set")


@pytest.fixture
def client():
    return Client(
        token=TOKEN,
        remote=REMOTE
    )


@liveonly
def test_indicator_search_fqdn(client):
    sleep(3)
    INDICATOR = 'example123123123.com'

    # create feed and test created feed
    f = Feed(client).new(USER, FEED, description='build search test feed')
    assert f['updated_at']

    # create test and submit test indicator
    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'indicator': INDICATOR,
        'comment': 'this is a test comment'
    })
    r = i.submit()

    # test creating the indicator
    assert r['indicator'] == INDICATOR
    assert r['itype'] == 'fqdn'
    assert r['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r:
        if record['feed'] == 'live-test-feed':
            assert record['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_search_ipv4(client):
    sleep(3)
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
    assert r['indicator'] == INDICATOR
    assert r['itype'] == 'ipv4'
    assert r['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r:
        if record['feed'] == 'live-test-feed':
            assert record['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_search_ipv6(client):
    sleep(3)
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
    assert r['indicator'] == INDICATOR
    assert r['itype'] == 'ipv6'
    assert r['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r:
        if record['feed'] == 'live-test-feed':
            assert record['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_search_email(client):
    sleep(3)
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
    assert r['indicator'] == INDICATOR
    assert r['itype'] == 'email'
    assert r['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r:
        if record['feed'] == 'live-test-feed':
            assert record['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_search_url(client):
    sleep(3)
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
    assert r['indicator'] == INDICATOR
    assert r['itype'] == 'uri'
    assert r['created_at']

    # search for indicator
    s = Search(client)
    r = s.search(INDICATOR, 10)
    for record in r:
        if record['feed'] == 'live-test-feed':
            assert record['indicator'] == INDICATOR

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200
