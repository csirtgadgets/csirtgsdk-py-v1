import pytest
import os
from pprint import pprint
from csirtgsdk.feed import Feed
from csirtgsdk.client import Client

CI_BUILD = os.environ.get('CI_BUILD', False)
TOKEN = os.environ.get('CSIRTG_TOKEN', None)
USER = os.environ.get('CSIRTG_USER', 'wes')
REMOTE = os.environ.get('CSIRTG_REMOTE', 'https://csirtg.io/api')

liveonly = pytest.mark.skipif(CI_BUILD is False, reason="CI_BUILD env var not set")

@pytest.fixture
def client():
    return Client(
        token=TOKEN,
        remote=REMOTE
    )

@liveonly
def test_create_feed(client):
    # make sure feed isnt left over from a previous run
    f = Feed(client).remove(USER, 'CI_BUILD_TEST')

    f = Feed(client).new(USER, 'CI_BUILD_TEST', description='test build feed')

    assert f['created_at']

    f = Feed(client).remove(USER, 'CI_BUILD_TEST')

    assert f == 200


@liveonly
def test_feed(client):
    f = Feed(client)

    assert f.client
