import logging
import base64
import hashlib
from csirtg_indicator import Indicator as I
import os.path
import json

from csirtgsdk.client.http import HTTP as Client


class Indicator(object):
    """
    Represents an Indicator object
    https://github.com/csirtgadgets/csirtgsdk/wiki/API#indicators
    """
    def __init__(self, kwargs):
        """
        :param client: csirtgsdk.client.Client object
        :param kwargs: dict of Indicator
        :return: Indicator object

        Example:
            Indicator({
                'indicator': 'example.org',
                'tags': 'botnet',
                'lasttime': '2015-01-01T00:00:59Z',
                'comment': 'example comment',
                'attachment': '/tmp/malware.zip'
            }).create()
        """

        self.logger = logging.getLogger(__name__)
        self.client = Client()

        required = {'user', 'feed'}

        if kwargs is None or len(required - set(kwargs.keys())) > 0:
            raise Exception("invalid arguments. missing: {}"
                            .format(required-set(kwargs.keys())))

        self.user = kwargs.pop('user')
        self.feed = kwargs.pop('feed')
        self.comment = kwargs.pop('comment', None)
        self.content = kwargs.pop('content', None)
        self.attachment = kwargs.pop('attachment', None)
        self.attachment_name = kwargs.pop('attachment_name', None)

        self.indicator = I(**kwargs)

    def show(self, user, feed, id):
        """
        Show a specific indicator by id

        :param user: feed username
        :param feed: feed name
        :param id: indicator endpoint id [INT]
        :return: dict

        Example:
            ret = Indicator.show('csirtgadgets','port-scanners', '1234')
        """
        uri = '/users/{}/feeds/{}/indicators/{}'.format(user, feed, id)
        return self.client.get(uri)

    def _file_to_attachment(self, blob, filename=None):
        """

        :param blob: a local file path or base64 encoded blob
        :param filename: file path
        :return: dict of base64 encoded filestring, with orig filename
        """

        if os.path.isfile(blob):
            filename = blob
            with open(blob,'rb') as f:
                data = f.read()
        else:
            if filename is None:
                raise RuntimeError('missing filename')
            try:
                data = base64.b64decode(blob)
            except TypeError:
                raise RuntimeError('attachment must be base64 encoded')

        md5 = hashlib.md5(data).hexdigest()
        sha1 = hashlib.sha1(data).hexdigest()
        sha256 = hashlib.sha256(data).hexdigest()
        sha512 = hashlib.sha512(data).hexdigest()
        data = base64.b64encode(data).decode('utf-8')

        return {
            'data': data,
            'filename': filename,
            'sha1': sha1,
            'md5': md5,
            'sha256': sha256,
            'sha512': sha512
        }

    def comments(self, user, feed, id):
        """
        Return comments for a specific indicator id

        :param user: feed username
        :param feed: feed name
        :param id: indicator id [INT]
        :return: list

        Example:
            ret = Indicator.comments('csirtgadgets','port-scanners', '1234')
        """
        uri = '/users/{}/feeds/{}/indicators/{}/comments'\
            .format(user, feed, id)
        return self.client.get(uri)

    def create(self):
        """
        Submit action on the Indicator object

        :return: Indicator Object
        """
        uri = '/users/{0}/feeds/{1}/indicators'\
            .format(self.user, self.feed)

        data = {
            "indicator": json.loads(str(self.indicator)),
            "comment": self.comment,
            "content": self.content
        }

        if self.attachment:
            attachment = self._file_to_attachment(
                self.attachment, filename=self.attachment_name)

            data['attachment'] = {
                'data': attachment['data'],
                'filename': attachment['filename']
            }

        if not data['indicator'].get('indicator'):
            data['indicator']['indicator'] = attachment['sha1']

        if not data['indicator'].get('indicator'):
            raise Exception('Missing indicator')

        return self.client.post(uri, data)

    def create_bulk(self, indicators, user, feed):
        from .constants import API_VERSION
        if API_VERSION == '1':
            print("create_bulk currently un-avail with APIv1")
            raise SystemExit

        """
        Submit action against the IndicatorBulk endpoint

        :param indicators: list of Indicator Objects
        :param user: feed username
        :param feed: feed name
        :return: list of Indicator Objects submitted

        from csirtgsdk.client import Client
        from csirtgsdk.indicator import Indicator

        remote = 'https://csirtg.io/api'
        token = ''
        verify_ssl = True

        i = {
            'indicator': 'example.com',
            'feed': 'test',
            'user': 'admin',
            'comment': 'this is a test',
        }

        data = []

        cli = Client(remote=remote, token=token, verify_ssl=verify_ssl)

        for x in range(0, 5):
            data.append(
                Indicator(cli, i)
            )

        ret = cli.submit_bulk(data, 'csirtgadgets', 'test-feed')
        """

        uri = '/users/{0}/feeds/{1}/indicators_bulk'.format(user, feed)

        data = {
            'indicators': [
                {
                    'indicator': i.args.indicator,
                    'feed_id': i.args.feed,
                    'tag_list': i.args.tags,
                    "description": i.args.description,
                    "portlist": i.args.portlist,
                    "protocol": i.args.protocol,
                    'firsttime': i.args.firsttime,
                    'lasttime': i.args.lasttime,
                    'portlist_src': i.args.portlist_src,
                    'comment': {
                        'content': i.args.comment
                    },
                    'rdata': i.args.rdata,
                    'rtype': i.args.rtype,
                    'content': i.args.content,
                    'provider': i.args.provider,
                } for i in indicators
                ]
        }
        return self.client.post(uri, data)

    submit = create
    submit_bulk = create_bulk
