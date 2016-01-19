import pytest

from csirtgsdk.client import Client


def test_client():
    c = Client(token=1234, remote='https://localhost2:8443', verify_ssl=False)

    assert c.remote == 'https://localhost2:8443', 'remote incorrect'
    assert c.verify_ssl is False, 'no-verify-ssl incorrect'
    assert c.token == str(1234), 'token mis-match'