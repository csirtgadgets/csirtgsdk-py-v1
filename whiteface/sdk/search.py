from whiteface.sdk.client import Client


class Search(Client):

    def __init__(self, **kwargs):
        super(Search, self).__init__(**kwargs)

        self.search = kwargs.get('search')

    def index(self):
        uri = self.remote + '/search?q={0}'.format(self.search)
        body = self._get(uri)
        body = {
            "feed": {
                "observables": body
            }
        }
        return body