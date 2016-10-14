from csirtgsdk.format.zbro import Bro
from pprint import pprint

def test_format_bro():
    data = [
        {
            'indicator': "example.com",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'itype': 'fqdn',
            'user': 'wes',
            'feed': 'test'
        },
        {
            'indicator': "http://example.com/1234.htm",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'itype': 'url',
            'user': 'wes',
            'feed': 'test'
        },
        {
            'indicator': "https://example.com/1234.htm",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'itype': 'url',
            'user': 'wes',
            'feed': 'test'
        },
        {
            'indicator': "192.168.1.1",
            'provider': "me.com",
            'tlp': "amber",
            'confidence': "85",
            'reporttime': '2015-01-01T00:00:00Z',
            'itype': 'ipv4',
            'user': 'wes',
            'feed': 'test'
        }
    ]
    l = []
    for d in data:
        l.append({'indicator': d})
    data = l
    data = {'feed': {'indicators': data}}

    text = str(Bro(data))
    print(text)
    assert text

if __name__ == '__main__':
    test_format_bro()
