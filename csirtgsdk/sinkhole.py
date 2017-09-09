import logging
import json
from pprint import pprint


class Sinkhole(object):
    """
    Sinkhole Object class
    """
    def __init__(self, client):
        """

        :param client: client.Client object
        :return: Search Object
        """
        self.logger = logging.getLogger(__name__)
        self.client = client

    def post(self, data):
        """
        POSTs a raw SMTP message to the Sinkhole API

        :param data: raw content to be submitted [STRING]
        :return: { list of predictions }
        """
        uri = '{}/sinkhole'.format(self.client.remote)
        self.logger.debug(uri)

        data = {
            'message': data
        }

        body = self.client.post(uri, data)
        return body
