import utils
import arrow
import logging


class Observable(object):

    def __init__(self, client, args):

        self.logger = logging.getLogger(__name__)
        self.client = client

        required = set(['user', 'feed', 'observable'])

        if args is None or len(required - set(args.keys())) > 0:
            raise Exception("invalid arguments. missing: {}"
                            .format(required-set(args.keys())))

        self.args = utils.Map(args)

        if self.args.tags and isinstance(self.args.tags, basestring):
            self.args.tags = self.args.tags.split(',')

        if self.args.firsttime:
            self.args.firsttime = arrow.get(self.args.firsttime).strftime("%Y-%m-%dT%H:%M:%S.%fZ").timestamp()

        if self.args.lasttime:
            self.args.lasttime = arrow.get(self.args.lasttime).strftime("%Y-%m-%dT%H:%M:%S.%fZ").timestamp()

    def show(self, user, feed, id):
        uri = '/users/{}/feeds/{}/observables/{}'.format(user, feed, id)
        return self.client.get(uri)

    def comments(self, user, feed, id):
        uri = '/users/{}/feeds/{}/observables/{}/comments'.format(user, feed, id)
        return self.client.get(uri)

    def submit(self):
        uri = '/users/{0}/feeds/{1}/observables'.format(self.args.user, self.args.feed)

        data = {
            "observable": {
                "thing": self.args.observable,
                "tags": self.args.tags,
                "portlist": self.args.portlist,
                "protocol": self.args.protocol,
                'firsttime': self.args.firsttime,
                'lasttime': self.args.lasttime
            },
            "comment": { 'text': self.args.comment }
        }

        return self.client.post(uri, data)
