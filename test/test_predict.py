import pytest
import os

from csirtgsdk.predict import Predict
from csirtgsdk.client import Client

CI_BUILD = os.environ.get('CI_BUILD', False)
TOKEN = os.environ.get('CSIRTG_TOKEN', None)
USER = os.environ.get('CSIRTG_USER', 'wes')
REMOTE = os.environ.get('CSIRTG_REMOTE', 'https://csirtg.io/api')

liveonly = pytest.mark.skipif(CI_BUILD is False, reason="CI_BUILD env var not set")

@pytest.fixture
def client():
    return Client()


def test_predict():
    client = Client()
    f = Predict(client)

    assert f.client


@liveonly
def test_predict_live():
    client = Client(
        token=TOKEN,
        remote=REMOTE
    )

    assert Predict(client).get("http://example.com")

    assert not Predict(client).get("http://ren-isac.net")
