# CSIRTG Software Development Kit for Python
The CSIRTG Software Development Kit (SDK) for Python contains library code and examples designed to enable developers to build applications using https://csirtg.io.

# Installation
## Ubuntu
  ```bash
  $ sudo apt-get install -y python-dev python-pip git
  $ pip install csirtgsdk
  ```

# Examples
## CLI
## Examples
### Search for an indicator
  ```bash
  $ export CSIRTG_TOKEN=1234..
  $ csirtg --search example.com
  ```
### Show a list of feeds (per user)
  ```bash
  $ export CSIRTG_TOKEN=1234..
  $ csirtg --user csirtgadgets --feeds
  ```
### Get a feed
  ```bash
  $ export CSIRTG_TOKEN=1234..
  $ csirtg --user csirtgadgets --feed uce-urls
  ```
### Create a feed
  ```bash
  $ csirtg --user csirtgadgets --new --feed scanners --description 'a feed of port scanners'
  ```
### Create an indicator within a feed
  ```bash
  $ csirtg --user csirtgadgets --feed scanners --new --indicator 1.1.1.1 --tags scanner --comment 'this is a port scanner'
  ```

### Create an attachment within a feed
  ```bash
  $ csirtg --user csirtgadgets --feed uce-attachments --new --attachment 'fax.zip' --description 'file attached in uce email'
  ```

## SDK
### QuickStart
#### Pulling a Feed
```bash
$ export CSIRTG_TOKEN=1234..
```
```python
from pprint import pprint
from csirtgsdk import feed
rv = feed('csirtgadgets/correlated')
pprint(rv)

{'created_at': '2018-01-17 22:05:04 UTC',
 'description': 'observed across multiple users feeds',
 'indicators': [{'asn': 7922.0,
                 'asn_desc': 'COMCAST CABLE COMMUNICATIONS, LLC',
                 'cc': 'US ',
                 'content': None,
                 'count': 3,
                 'created_at': '2018-10-14 14:53:13 UTC',
                 'description': 'correlated',
                 'firsttime': '2018-10-14 00:11:28 UTC',
                 'id': 12645415,
                 'indicator': '98.220.252.135',
                 'itype': 'ipv4',
                 'lasttime': '2019-01-13 04:03:45 UTC',
                 'portlist': None,
                 'provider': None,
                 'tags': ['login', 'photon', 'hacking', 'telnet', 'scanner'],
                 'updated_at': '2019-01-13 20:59:01 UTC'},
                 ...


```

#### Searching for an Indicator
```python
from pprint import pprint
from csirtgsdk import search
rv = search('exmple.com')
pprint(rv)

[{'attachments': [],
  'comments': [],
  'created_at': '2018-01-31 11:34:30 UTC',
  'feed': 'uce-email-addresses',
  'indicator': 'maria84400@untangle.example.com',
  'lasttime': '2018-01-31 11:34:30 UTC',
  'license': {'name': 'CC BY-SA 4.0',
              'url': 'http://creativecommons.org/licenses/by-sa/4.0/'},
  'location': 'https://csirtg.io/users/csirtgadgets/feeds/uce-email-addresses',
  'portlist': None,
  'tags': ['email-address', 'uce'],
  'updated_at': '2018-01-31 11:34:30 UTC',
  'user': 'csirtgadgets'},
  ...
```

#### Create an Indicator
```python
from pprint import pprint
from csirtgsdk import indicator_create
i = {'indicator': 'example.com', 'tags': ['ssh'], 'description': 'this is a test'}
rv = indicator_create('wes/test',i)

{'asn': 15133.0,
 'asn_desc': 'MCI COMMUNICATIONS SERVICES, INC. D/B/A VERIZON BUSINESS',
 'cc': 'US',
 'content': None,
 'count': 1,
 'created_at': '2019-01-13 21:06:13 UTC',
 'description': 'this is a test',
 'feed': 'test',
 'firsttime': '2019-01-13 21:06:13 UTC',
 'id': 13205300,
 'indicator': 'example.com',
 'itype': 'fqdn',
 'lasttime': '2019-01-13 21:06:13 UTC',
 'license': {'name': 'CC BY-SA 4.0',
             'url': 'http://creativecommons.org/licenses/by-sa/4.0/'},
 'location': 'https://csirtg.io/users/wes/feeds/test/indicators/13205300',
 'portlist': None,
 'portlist_src': None,
 'protocol': None,
 'provider': None,
 'updated_at': '2019-01-13 21:06:13 UTC',
 'user': 'wes'}

```

### Advanced SDK
#### Search for an indicator

  ```python
  from csirtgsdk.client import Client
  from csirtgsdk.search import Search
  from pprint import pprint
  
  remote = 'https://csirtg.io/api'
  token = ''
  verify_ssl = True
  limit = 500
  
  indicator = 'example'
  
  # Initiate client object
  cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)
  
  # Search for an indicator
  ret = Search(cli).search(indicator, limit=limit)
  
  # pretty print the returned data structure
  pprint(ret)
  ```
  
#### Show a list of feeds (per user)
  ```python
  from csirtgsdk.client import Client
  from csirtgsdk.feed import Feed
  from pprint import pprint
  
  remote = 'https://csirtg.io/api'
  token = ''
  verify_ssl = True
  
  user = 'csirtgadgets'
  
  # Initiate client object
  cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)
  
  # Return a list of feeds (per user)
  ret = Feed(cli).index(user)
  
  # pprint the returned data structure
  pprint(ret)
  ```

#### Get a feed
  ```python
  from csirtgsdk.client import Client
  from csirtgsdk.feed import Feed
  from pprint import pprint
  
  remote = 'https://csirtg.io/api'
  token = ''
  verify_ssl = True
  
  user = 'csirtgadgets'
  feed = 'uce-urls'
  
  # Initiate client object
  cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)
  
  # Pull a feed
  ret = Feed(cli).show(user, feed, limit=None)
  
  # pprint the returned data structure
  pprint(ret)
  ```
  
#### Create a feed
  ```python
  from csirtgsdk.client import Client
  from csirtgsdk.feed import Feed
  from pprint import pprint
  
  remote = 'https://csirtg.io/api'
  token = ''
  verify_ssl = True
  
  user = 'csirtgadgets'
  feed = 'scanners'
  feed_description = 'a feed of port scanners'
  
  # Initiate client object
  cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)
  
  # Create a feed
  ret = Feed(cli).new(user, feed, description=feed_description)
  
  # pprint the returned data structure
  pprint(ret)
  ```
  
#### Submit a indicator to a feed  
```python
from csirtgsdk.client import Client
from csirtgsdk.indicator import Indicator
from pprint import pprint

remote = 'https://csirtg.io/api'
token = ''
verify_ssl = True

record = {
  "user": "csirtgadgets",
  "feed": "scanners",
  "indicator": "1.1.1.1",
  "tags": "scanner",
  "description": "seen port scanning (incomming, tcp, syn, blocked)",
  "portlist": "22",
  "protocol": "TCP",
  "firsttime": "2015-11-22T00:00:00Z",
  "lasttime": "2015-11-23T00:00:00Z",
  "comment": "comment text",
  "attachment": "/tmp/malware.zip"
}

# Initiate client object
cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)

# Submit an indicator
ret = Indicator(cli, record).submit()

# pprint the returned data structure
pprint(ret)
```

#### Submit a list of indicators to a feed
```python
from csirtgsdk.client import Client                                                                                                                                                                                    
from csirtgsdk.indicator import Indicator
from pprint import pprint

remote = 'https://csirtg.io/api'
token = ''
verify_ssl = True

user = 'csirtgadgets'
feed = 'test-feed'

i = {
    'indicator': 'example.com',
    'feed': 'csirtgadgets',
    'user': 'test-feed',
    'comment': 'this is a test',
}

data = []

# Initiate client object
cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)

# Build a list of Indicator objects
for x in range(0, 5):
    data.append(
        Indicator(cli, i)
    )

# Call the submit bulk function
ret = cli.submit_bulk(data, user, feed)

# Print the return value
pprint(ret)

{u'message': u'5 indicators received'}
```
  
#### Submit a file to a feed using a filehandle
```python
from csirtgsdk.client import Client
from csirtgsdk.indicator import Indicator
from pprint import pprint

filename = '/tmp/sample.txt'

remote = 'https://csirtg.io/api'
token = ''
verify_ssl = True

# read the file
with open(filename) as f:
   data = f.read()

# Create a dict to submit
record = {
   'user': 'csirtgadgets',
   'feed': 'uce-attachments',
   'tags': 'uce-attachment',
   'description': 'file attached to spam email',
   'attachment': filename
}

# Initiate client object
cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)

# Submit an indicator
ret = Indicator(cli, record).submit()

# pprint the returned data structure
pprint(ret)
```

#### Submit a file to a feed using a base64 encoded string
```python
import hashlib
import base64
from csirtgsdk.client import Client
from csirtgsdk.indicator import Indicator
from pprint import pprint

filename = '/tmp/sample.txt'

remote = 'https://csirtg.io/api'
token = ''
verify_ssl = True

# read the file
with open(filename) as f:
  data = f.read()

# Create a dict to submit
record = {
  'user': 'csirtgadgets',
  'feed': 'uce-attachments',
  'indicator': hashlib.sha1(data).hexdigest(),
  'tags': 'uce-attachment',
  'description': 'file attached to spam email',
  'attachment': base64.b64encode(data),
  'attachment_name': filename
}

# Initiate client object
cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)

# Submit an indicator
ret = Indicator(cli, record).submit()

# pprint the returned data structure
pprint(ret)
```


# License and Copyright

Copyright (C) 2019 [CSIRT Gadgets](http://csirtgadgets.com)

Free use of this software is granted under the terms of the [MPL2 License](https://www.mozilla.org/en-US/MPL/2.0/). For details see the file ``LICENSE`` included with the distribution.
