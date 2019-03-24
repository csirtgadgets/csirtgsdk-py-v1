import pytest

from csirtgsdk.sinkhole import Sinkhole
from csirtgsdk.client.http import HTTP as Client


@pytest.fixture
def client():
    return Client()


def test_search(client):
    f = Sinkhole(client)

    assert f.client
