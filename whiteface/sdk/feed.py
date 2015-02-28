from whiteface.sdk.client import Client


class Feed(Client):

    def __init__(self, **kwargs):
        super(Feed, self).__init__(**kwargs)

        self.user = kwargs.get('user')
        self.name = kwargs.get('name') or kwargs.get('feed')

    def new(self):
        uri = self.remote + '/users/{0}/feeds'.format(self.user)

        data = {
            'feed': {
                'name': self.name
            }
        }

        body = self._post(uri, data)
        if body.get('feed'):
            return body['feed']

        return body

    def index(self):
        uri = self.remote + '/users/{0}/feeds'.format(self.user)
        return self._get(uri)

    def show(self):
        uri = self.remote + '/users/{0}/feeds/{1}'.format(self.user, self.name)
        return self._get(uri)