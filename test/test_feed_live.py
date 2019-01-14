import pytest
import os
from pprint import pprint
from time import sleep
from csirtgsdk.feed import Feed
from csirtgsdk.client.http import HTTP as Client

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
    sleep(3)
    # make sure feed isnt left over from a previous run
    f = Feed(client).remove(USER, 'ci_build_test')

    f = Feed(client).new(USER, 'ci_build_test', description='test build feed')

    assert f['created_at']

    f = Feed(client).remove(USER, 'ci_build_test')

    assert f == 200


@liveonly
def test_feed(client):
    f = Feed(client)

    assert f.client
