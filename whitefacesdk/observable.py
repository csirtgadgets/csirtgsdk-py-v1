
import arrow
import logging
import base64


class Observable(object):

    def __init__(self, client, thing, user=None, feed=None, comment=None, tags=None, portlist=None, protocol=None,
                 firsttime=None, lasttime=None, attachment=None):
        '''
        :param client:
        :param thing:
        :param user:
        :param feed:
        :param comment:
        :param tags:
        :param portlist:
        :param protocol:
        :param firsttime:
        :param lasttime:
        :param attachment: filename of an attachment
        :return:
        '''

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

        self.attachment = attachment

        if firsttime:
            self.firsttime = arrow.get(firsttime).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        if lasttime:
            self.lasttime = arrow.get(lasttime).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def show(self, user, feed, id):
        uri = '/users/{}/feeds/{}/observables/{}'.format(user, feed, id)
        return self.client.get(uri)

    def _file_to_attachment(self, filename):
        '''

        :param filename:
        :return: dict of base64 encoded filestring, with orig filename
        '''
        import base64

        with open(filename) as f:
            data = f.read()

        data = base64.b64encode(data)
        return {
            'data': data,
            'filename': filename,
        }

    def comments(self, user, feed, id):
        uri = '/users/{}/feeds/{}/observables/{}/comments'.format(user, feed, id)
        return self.client.get(uri)

    def new(self, user, feed):
        '''
        :param user: username
        :param feed: feed name
        :return:
        '''
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

            "comment": {
                'text': self.comment,
            }
        }

        if self.attachment:
            self.logger.debug('adding attachment')
            attachment = self._file_to_attachment(self.attachment)
            data['comment']['attachment'] = attachment

        return self.client.post(uri, data)
