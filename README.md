# WhiteFace Software Development Kit for Python
The WhiteFace Software Development Kit (SDK) for Python contains library code and examples designed to enable developers to build applications using WhiteFace.

# Installation
## Ubuntu
  ```bash
  $ apt-get install -y python-dev python-pip git
  $ pip install https://github.com/csirtgadgets/py-whitefacesdk/archive/master.tar.gz
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

# Documentation

http://py-whitefacesdk.readthedocs.org/


# License and Copyright

Copyright (C) 2015 [CSIRT Gadgets](http://csirtgadgets.com)

Free use of this software is granted under the terms of the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl.html) (LGPL v3.0). For details see the file ``LICENSE`` included with the distribution.
