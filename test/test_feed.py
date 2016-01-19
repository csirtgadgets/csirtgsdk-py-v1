import pytest

from csirtgsdk.feed import Feed
from csirtgsdk.client import Client

@pytest.fixture
def client():
    return Client()


def test_feed(client):
    f = Feed(client)

    assert f.client