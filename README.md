# WhiteFace Software Development Kit for Python
The WhiteFace Software Development Kit (SDK) for Python contains library code and examples designed to enable developers to build applications using WhiteFace.

# Installation
## Ubuntu
  ```bash
  sudo apt-get install -y python-dev python-pip git
  sudo pip install git+https://github.com/csirtgadgets/py-whiteface-sdk.git
  ```

# Examples
## Client
### Config
  ```yaml
  # ~/.wf.yml
  token: 1234
  ```
### Running
  ```bash
  $ wf --search badsite.com
  $ wf --user wes --feed spyeye
  $ wf --user wes --feed-create zeus
  $ wf --user wes --feed zeus --observable-create --thing badsite.com --tags zeus,bot --comment 'this is a really bad guy...'
  ```

## API
### search
```python
  from whiteface.sdk.client import Client
  from whiteface.sdk.format.table import Table
  
  cli = Client(token=options['token'])
  ret = cli.search('1.2.3.4')
  print Table(data=ret)
  
```

### feed
```python
  from whiteface.sdk.client import Client
  from whiteface.sdk.format.table import Table
  
  options = {
    "token": "1234",
    "user": "wes",
    "feed": "scanners"
  }

  cli = Client(token=options['token'])

  ret = cli.feed(user=options['user'], feed=options['feed'])
  print Table(data=ret)
```
 
### feed_create
```python
  from whiteface.sdk.client import Client
  
  cli = Client(token="1234")
  
  cli.feed_create(name='my zeus feed'))
```

### observable
```python
  from whiteface.sdk.client import Client
  from whiteface.sdk.format.table import Table
    
  ret = cli.observables('example.com', username=None)
  print Table(data=ret)
```

### observable_create
```python
  from whiteface.sdk.client import Client
  
  obs = {
    "thing": "example.com",
    "tags": ['zeus','bot'],
  }
  cli.observable_create(feed, thing, tags=[], comment=None)
```

# License and Copyright

Copyright (C) 2015 [CSIRT Gadgets](http://csirtgadgets.com)

Free use of this software is granted under the terms of the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html) (LGPL v3.0). For details see the file ``LICENSE`` included with the distribution.
