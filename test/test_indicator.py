import pytest

from csirtgsdk.indicator import Indicator
from csirtgsdk.client import Client

@pytest.fixture
def client():
    return Client()


def test_indicator(client):
    f = Indicator(client, {
        'feed': 'testfeed',
        'user': 'testuser',
        'indicator': 'example.com',
        'tags': ['tag1', 'tag2']
    })

    assert f.client
    assert f.args.indicator == 'example.com'