# WhiteFace Software Development Kit for Python
The WhiteFace Software Development Kit (SDK) for Python contains library code and examples designed to enable developers to build applications using WhiteFace.

# Installation
## Ubuntu
  ```bash
  $ apt-get install -y python-dev python-pip git
  $ sudo pip install pip --upgrade  # requires > 6.2
  $ pip install https://github.com/csirtgadgets/py-whitefacesdk/archive/master.tar.gz
  ```

# Examples
## CLI
### Config
  ```yaml
  # ~/.wf.yml
  token: 1234
  ```
## Examples
### Search for an observable
  ```bash
  $ wf --search example.com
  ```
### Show a list of feeds (per user)
  ```bash
  $ wf --user csirtgadgets --feeds
  ```
### Get a feed
  ```bash
  $ wf --user csirtgadgets --feed uce-urls
  ```
### Create a feed
  ```bash
  $ wf --user csirtgadgets --new --feed scanners --description 'a feed of port scanners'
  ```
### Create an observable within a feed
  ```bash
  $ wf --user csirtgadgets --feed scanners --new --observable 1.1.1.1 --tags scanner --comment 'this is a port scanner'
  ```

## SDK
### Search for an observable

  ```python
  from whitefacesdk.client import Client
  from whitefacesdk.search import Search
  from pprint import pprint
  
  remote = 'https://whiteface.csirtgadgets.com/api'
  token = ''
  verify_ssl = True
  limit = 500
  
  observable = 'example'
  
  # Initiate client object
  cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)
  
  # Search for an observable
  ret = Search(cli).search(observable, limit=limit)
  
  # pretty print the returned data structure
  pprint(ret)
  ```
  
### Show a list of feeds (per user)
  ```python
  from whitefacesdk.client import Client
  from whitefacesdk.feed import Feed
  from pprint import pprint
  
  remote = 'https://whiteface.csirtgadgets.com/api'
  token = ''
  verify_ssl = True
  limit = 500
  
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
  from whitefacesdk.client import Client
  from whitefacesdk.feed import Feed
  from pprint import pprint
  
  remote = 'https://whiteface.csirtgadgets.com/api'
  token = ''
  verify_ssl = True
  limit = 500
  
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
  from whitefacesdk.client import Client
  from whitefacesdk.feed import Feed
  from pprint import pprint
  
  remote = 'https://whiteface.csirtgadgets.com/api'
  token = ''
  verify_ssl = True
  limit = 500
  
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
  
### Create an observable within a feed  
  ```python
  from whitefacesdk.client import Client
  from whitefacesdk.observable import Observable
  from pprint import pprint
  
  remote = 'https://whiteface.csirtgadgets.com/api'
  token = ''
  verify_ssl = True
  limit = 500
  
  record = {
      "user": "csirtgadgets",
      "feed": "scanners",
      "observable": "1.1.1.1",
      "tags": "scanner",
      "description": "seen port scanning (incomming, tcp, syn, blocked)",
      "portlist": "22",
      "protocol": "TCP",
      "firsttime": "2015-11-22T00:00:00Z",
      "lasttime": "2015-11-23T00:00:00Z",
      "comment": {'text': "comment text"}
  }
  
  # Initiate client object
  cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)
  
  # Submit an observable
  ret = Observable(cli, record).submit()
  
  # pprint the returned data structure
  pprint(ret)
  ```

# Documentation

http://py-whitefacesdk.readthedocs.org/


# License and Copyright

Copyright (C) 2015 [CSIRT Gadgets](http://csirtgadgets.com)

Free use of this software is granted under the terms of the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html) (LGPL v3.0). For details see the file ``LICENSE`` included with the distribution.
