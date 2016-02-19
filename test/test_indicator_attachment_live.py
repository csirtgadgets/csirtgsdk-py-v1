import pytest
import os
from pprint import pprint
from csirtgsdk.indicator import Indicator
from csirtgsdk.feed import Feed
from csirtgsdk.client import Client

CI_BUILD = os.environ.get('CI_BUILD', False)
TOKEN = os.environ.get('CSIRTG_TOKEN', None)
USER = os.environ.get('CSIRTG_USER', 'wes')
REMOTE = os.environ.get('CSIRTG_REMOTE', 'https://csirtg.io/api')
FEED = os.environ.get('CSIRTG_FEED', 'CI_ATTACHMENT_TEST')

liveonly = pytest.mark.skipif(CI_BUILD is False, reason="CI_BUILD env var not set")

@pytest.fixture
def client():
    return Client(
        token=TOKEN,
        remote=REMOTE
    )


@liveonly
def test_indicator_attachment_zip(client):
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/malware.jar.zip',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    assert r['indicator']['indicator'] == '8b71e770f763d2c57aa6f6c8dcb55645d57b9096'
    assert r['indicator']['attachments'][0]['attachment']
    assert r['indicator']['attachments'][0]['filesize']
    assert r['indicator']['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200


@liveonly
def test_indicator_attachment_jar(client):
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/malware.jar',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    assert r['indicator']['indicator'] == '2097a35058b337aa4c8b3bafdb6ecc7b8dc4df5c'
    assert r['indicator']['attachments'][0]['attachment']
    assert r['indicator']['attachments'][0]['filesize']
    assert r['indicator']['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200

@liveonly
def test_indicator_attachment_docx(client):
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/c..docx',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    assert r['indicator']['indicator'] == '3758401d18b855f33777c5081f9a0c1836be44e3'
    assert r['indicator']['attachments'][0]['attachment']
    assert r['indicator']['attachments'][0]['filesize']
    assert r['indicator']['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200

@liveonly
def test_indicator_attachment_doc(client):
    f = Feed(client).new(USER, FEED, description='test build feed')

    assert f['created_at']

    i = Indicator(client, {
        'user': USER,
        'feed': FEED,
        'attachment': 'samples/business_relationship.doc',
        'comment': 'asdfasdfasdf'
    })
    r = i.submit()

    assert r['indicator']['indicator'] == 'a8f4c8f7a410af30f871cb4ab61aaaeb6714210e'
    assert r['indicator']['attachments'][0]['attachment']
    assert r['indicator']['attachments'][0]['filesize']
    assert r['indicator']['attachments'][0]['created_at']

    # delete test feed
    f = Feed(client).remove(USER, FEED)
    assert f == 200