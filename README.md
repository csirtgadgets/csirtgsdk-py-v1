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
### Config
  ```yaml
  # ~/.csirtg.yml
  token: 1234
  ```
## Examples
### Search for an indicator
  ```bash
  $ csirtg --search example.com
  ```
### Show a list of feeds (per user)
  ```bash
  $ csirtg --user csirtgadgets --feeds
  ```
### Get a feed
  ```bash
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
### Search for an indicator

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
  
### Show a list of feeds (per user)
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

### Get a feed
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
  
### Create a feed
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
  
### Submit a indicator to a feed  
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

### Submit a list of indicators to a feed
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
  
### Submit a file to a feed using a filehandle
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
   
### Submit a file to a feed using a base64 encoded string
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


# Documentation

http://py-csirtgsdk.readthedocs.org/


# License and Copyright

Copyright (C) 2015 [CSIRT Gadgets](http://csirtgadgets.com)

Free use of this software is granted under the terms of the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html) (LGPL v3.0). For details see the file ``LICENSE`` included with the distribution.
