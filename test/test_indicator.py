import pytest

from whitefacesdk.indicator import Indicator
from whitefacesdk.client import Client

@pytest.fixture
def client():
    return Client()


def test_indicator(client):
    f = Indicator(client, {'feed': 'testfeed', 'user': 'testuser', 'indicator': 'example.com'})

    assert f.client
    assert f.args.indicator == 'example.com'