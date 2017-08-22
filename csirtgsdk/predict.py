import logging
import json


class Predict(object):
    """
    Predict Object class
    """
    def __init__(self, client):
        """

        :param client: client.Client object
        :return: Search Object
        """
        self.logger = logging.getLogger(__name__)
        self.client = client

    def get(self, q, limit=None):
        """
        Performs a search against the predict endpoint

        :param q: query to be searched for [STRING]
        :return: { score: [0|1] }
        """
        uri = '{}/predict?q={}'.format(self.client.remote, q)
        self.logger.debug(uri)

        body = self.client.get(uri)
        return body['score']
