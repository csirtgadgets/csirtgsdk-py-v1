import pytest
import os

from csirtgsdk.predict import Predict
from time import sleep

CI_BUILD = os.environ.get('CI_BUILD', False)
TOKEN = os.environ.get('CSIRTG_TOKEN', None)
USER = os.environ.get('CSIRTG_USER', 'wes')
REMOTE = os.environ.get('CSIRTG_REMOTE', 'https://csirtg.io/api')

liveonly = pytest.mark.skipif(CI_BUILD is False, reason="CI_BUILD env var not set")


def test_predict():
    f = Predict()

    assert f.client


@liveonly
def test_predict_live():
    sleep(3)
    assert Predict().get("http://example.com") == 0

    assert not Predict().get("http://ren-isac.net")
