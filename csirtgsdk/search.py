import logging
from csirtgsdk.client.http import HTTP as Client


class Search(object):
    """
    Search Object class
    """
    def __init__(self, client=Client()):
        """

        :param client: client.Client object
        :return: Search Object
        """
        self.logger = logging.getLogger(__name__)
        self.client = client

    def search(self, q, limit=None):
        """
        Performs a search against the /search endpoint

        :param q: query to be searched for [STRING]
        :param limit: limit the results [INT]
        :return: list of dicts
        """
        uri = '{}/search'.format(self.client.remote)
        body = self.client.get(uri, {'q': q, 'limit': limit})
        return body
