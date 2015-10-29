import pytest

from whitefacesdk.search import Search
from whitefacesdk.client import Client

@pytest.fixture
def client():
    return Client()


def test_search(client):
    f = Search(client)

    assert f.client