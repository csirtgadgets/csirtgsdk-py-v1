# WhiteFace Software Development Kit for Python
The WhiteFace Software Development Kit (SDK) for Python contains library code and examples designed to enable developers to build applications using WhiteFace.

# Installation
## Ubuntu
  ```bash
  sudo apt-get install -y python-dev python-pip git
  git clone https://github.com/csirtgadgets/py-whiteface-sdk.git -b master
  cd py-whiteface-sdk
  pip install -r requirements.txt
  python setup.py build
  python setup.py test
  python setup.py install
  ```

# Examples
## Client
### Config
  ```yaml
  # ~/.wf.yml
  client:
    token: 1234
  ```
### Running
  ```bash
  $ wf --token 1234 --user wes --feed scanners
  ```

## API
### ping
  ```python
    from whiteface.sdk.client import Client
  
    options = {
        "token": "1234",
    }

    ret = cli.ping()
    
    print "roundtrip: %s ms" % ret
  ```

### feed
  ```python
    from whiteface.sdk.client import Client
    
    options = {
        "token": "1234",
        "user": "wes",
        "feed": "scanners"
    }

    cli = Client(token=options['token'])

    ret = cli.feed(user=options['user'], feed=options['feed'])
    print cli.table(data=ret)
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
    
    ret = cli.observables('example.com', username=None)
    print cli.table(data=ret)
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

# Support and Documentation

You can also look for information at the [GitHub repo](https://github.com/csirtgadgets/py-whiteface-sdk).

# License and Copyright

Copyright (C) 2015 [CSIRT Gadgets](http://csirtgadgets.com)

Free use of this software is granted under the terms of the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html) (LGPL v3.0). For details see the file ``LICENSE`` included with the distribution.
