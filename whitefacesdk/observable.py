
import arrow
import logging


class Observable(object):

    def __init__(self, client, thing, user=None, feed=None, comment=None, tags=None, portlist=None, protocol=None,
                 firsttime=None, lasttime=None):

        self.logger = logging.getLogger(__name__)
        self.client = client

        if tags and isinstance(tags, basestring):
            tags = tags.split(',')

        self.user = user
        self.feed = feed
        self.thing = thing

        self.comment = comment
        self.tags = tags
        self.portlist = portlist
        self.protocol = protocol
        self.firsttime = firsttime
        self.lasttime = lasttime

        if firsttime:
            self.firsttime = arrow.get(firsttime).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        if lasttime:
            self.lasttime = arrow.get(lasttime).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def show(self, user, feed, id):
        uri = '/users/{}/feeds/{}/observables/{}'.format(user, feed, id)
        return self.client.get(uri)

    def attachment(self, user, feed, observable, attachment, text=None):
        uri = '/users/{}/feeds/{}/observables/{}/comments'.format(user, feed, observable)
        data = {
            'comment': {
                'attachment': attachment,
            },
            #'user_id': user,
            #'feed_id': feed,
        }
        return self.post(uri, data)

    def comment(self, user, feed, text):
        pass

    def comments(self, user, feed, id):
        uri = '/users/{}/feeds/{}/observables/{}/comments'.format(user, feed, id)
        return self.client.get(uri)

    def new(self, user, feed):
        uri = '/users/{0}/feeds/{1}/observables'.format(user, feed)

        data = {
            "observable": {
                "thing": self.thing,
                "tags": self.tags,
                "portlist": self.portlist,
                "protocol": self.protocol,
                'firsttime': self.firsttime,
                'lasttime': self.lasttime
            },

            "comment": self.comment
        }

        return self.client.post(uri, data)
