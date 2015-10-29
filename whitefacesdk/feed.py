
class Feed(object):
    """
    Represents a Feed Object
    """
    def __init__(self, client):
        self.client = client

    def new(self, user, name, description=None):
        """
        Creates a new feed

        :return: dict
        """
        uri = self.client.remote + '/users/{0}/feeds'.format(user)

        data = {
            'feed': {
                'name': self.name,
                'description': self.description
            }
        }

        body = self.client._post(uri, data)
        if body.get('feed'):
            return body['feed']

        return body

    def index(self, user):
        """
        Returns a list of Feeds from the API

        :return: dict
        """
        uri = self.client.remote + '/users/{0}/feeds'.format(user)
        return self.client.get(uri)

    def show(self, user, name, limit=None):
        """
        Returns a specific Feed from the API

        :return: dict
        """
        uri = self.client.remote + '/users/{0}/feeds/{1}'.format(user, name)
        return self.client.get(uri, params={'limit': limit})