import pytest

from csirtgsdk.feed import Feed
from csirtgsdk.client.http import HTTP as Client

@pytest.fixture
def client():
    return Client()


def test_feed(client):
    f = Feed(client)

    assert f.client