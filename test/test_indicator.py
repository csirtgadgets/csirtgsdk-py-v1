import pytest

from csirtgsdk.indicator import Indicator


def test_indicator():
    f = Indicator({
        'feed': 'testfeed',
        'user': 'testuser',
        'indicator': 'example.com',
        'tags': ['tag1', 'tag2']
    })

    assert f.client
    assert f.indicator.indicator == 'example.com'
