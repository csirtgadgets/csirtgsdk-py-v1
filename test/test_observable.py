import pytest

from whitefacesdk.observable import Observable
from whitefacesdk.client import Client

@pytest.fixture
def client():
    return Client()


def test_observable(client):
    f = Observable(client, {'feed': 'testfeed', 'user': 'testuser', 'observable': 'example.com'})

    assert f.client
    assert f.args.observable == 'example.com'