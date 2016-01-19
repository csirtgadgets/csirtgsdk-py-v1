STIX_ENABLED = True

try:
    from stix.core import STIXHeader
    from csirtgsdk.format.format_stix import Stix
except ImportError:
    STIX_ENABLED = False

data = [
    {
        'indicator': "example.com",
        'reporttime': '2015-01-01T00:00:00Z',
        'tags': ['botnet', 'malware'],
        'provider': 'csirtg.com'
    },
    {
        'indicator': "192.168.1.1",
        'reporttime': '2015-01-01T00:00:00Z',
        'tags': ['botnet', 'malware'],
        'provider': 'csirtg.com'
    },
    {
        'indicator': "f98c7fffc3fe221e79fa19fe89c74e74c0da1266",
        'reporttime': '2015-01-01T00:00:00Z',
        'tags': ['botnet', 'malware'],
        'provider': 'csirtg.com'
    }
]


def test_stix():
    if STIX_ENABLED:
        d = Stix(data)
        assert len(str(d)) > 2
    else:
        print('STIX package not installed, skipping test')
