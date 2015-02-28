from whiteface import client


class Feed(client.Client):
    """
    Represents a Feed Object
    """
    def __init__(self, **kwargs):
        """
        name - feed name
        user - user name
        """
        super(Feed, self).__init__(**kwargs)

        self.user = kwargs.get('user')
        self.name = kwargs.get('name') or kwargs.get('feed')
        self.description = kwargs.get('description')

    def new(self):
        """
        Creates a new feed

        :return: dict
        """
        uri = self.remote + '/users/{0}/feeds'.format(self.user)

        data = {
            'feed': {
                'name': self.name,
                'description': self.description
            }
        }

        body = self._post(uri, data)
        if body.get('feed'):
            return body['feed']

        return body

    def index(self):
        """
        Returns a list of Feeds from the API

        :return: dict
        """
        uri = self.remote + '/users/{0}/feeds'.format(self.user)
        return self._get(uri)

    def show(self):
        """
        Returns a specific Feed from the API

        :return: dict
        """
        uri = self.remote + '/users/{0}/feeds/{1}'.format(self.user, self.name)
        return self._get(uri)