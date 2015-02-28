from whiteface import client


class Observable(client.Client):

    def __init__(self, **kwargs):
        super(Observable, self).__init__(**kwargs)

        try:
            self.user = kwargs['user']
        except:
            raise RuntimeError('missing user name')

        try:
            self.feed = kwargs['feed']
        except:
            raise RuntimeError('missing feed name')

        try:
            self.thing = kwargs['thing']
        except:
            raise RuntimeError('missing thing')

        self.comment = kwargs.get('comment')
        self.tags = kwargs.get('tags')
        self.portlist = kwargs.get('portlist')
        self.protocol = kwargs.get('protocol')

        if isinstance(self.tags, list):
            self.tags = ','.join(self.tags)

    def show(self):
        pass

    def comments(self):
        pass

    def new(self):
        uri = self.remote + '/users/{0}/feeds/{1}/observables'.format(self.user, self.feed)

        data = {
            "observable": {
                "thing": self.thing,
                "tags": self.tags,
                "portlist": self.portlist,
                "protocol": self.protocol,
            },

            "comment": self.comment
        }

        data = self._post(uri, data)
        return data