.. Csirtgsdk SDK documentation master file, created by
   sphinx-quickstart on Thu Oct 29 10:17:48 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the CSIRTG SDK documentation!
========================================

Contents:

.. toctree::
   :maxdepth: 2

   client.rst
   mysearch.rst
   feed.rst
   indicator.rst
   utils.rst


Examples
========

.. code-block:: bash

   $ csirtg --search example.com
   $ csirtg --user csirtgadgets --feeds
   $ csirtg --user csirtgadgets --feed uce-urls
   $ csirtg --user csirtgadgets --new --feed scanners --description 'a feed of port scanners'
   $ csirtg --user csirtgadgets --feed scanners --new --indicator 1.1.1.1 --tags scanner --comment 'this is a port scanner'

Search
======

.. code-block:: python

   from csirtgsdk.client import Client
   from csirtgsdk.search import Search
   from pprint import pprint

   # Initiate client object
   cli = Client(token=token)

   # Search for an indicator
   ret = Search(cli).search('example.org', limit=5)

   # short form
   ret = Search(Client(token=token)).search('example.org', limit=5)

   # pretty print the returned data structure
   pprint(ret)

Show Feed
=========

.. code-block:: python

   from csirtgsdk.client import Client
   from csirtgsdk.feed import Feed
   from pprint import pprint

   # Initiate client object
   cli = Client(token=token)

   # Pull a feed
   ret = Feed(cli).show('csirtgadgets', 'uce-urls')

   # pprint the returned data structure
   pprint(ret)

Create Feed
===========

.. code-block:: python

   from csirtgsdk.client import Client
   from csirtgsdk.feed import Feed
   from pprint import pprint

   # Initiate client object
   cli = Client(token=token)

   # Create a feed
   ret = Feed(cli).new('csirtgadgets', 'scanners', description='a feed of port scanners')

   # pprint the returned data structure
   pprint(ret)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

