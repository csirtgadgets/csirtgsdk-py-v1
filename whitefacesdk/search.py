import logging


class Search(object):

    def __init__(self, client):
        self.logger = logging.getLogger(__name__)
        self.client = client

    def search(self, q, limit=None):
        uri = '{}/search?q={}'.format(self.client.remote, q)
        self.logger.debug(uri)

        body = self.client.get(uri)
        body = {
            "feed": {
                "observables": body
            }
        }
        return body