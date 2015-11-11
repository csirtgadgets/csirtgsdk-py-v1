import utils
import arrow
import logging
import base64


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

        if self.args.attachment:
            del data['comment']
            self.logger.debug('adding attachment')
            attachment = self._file_to_attachment(self.args.attachment)
            data['comment']['attachment'] = attachment

        return self.client.post(uri, data)
