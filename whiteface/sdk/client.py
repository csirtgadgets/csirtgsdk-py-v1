import json
import requests
import time
import logging
import whiteface.sdk

from pprint import pprint

API_VERSION = whiteface.sdk.API_VERSION

REMOTE ='https://whiteface.csirtgadgets.com/api'
LIMIT = 5000
TIMEOUT = 300

class Client(object):

    def __init__(self, remote=REMOTE, logger=logging.getLogger(__name__),
                 token=None, proxy=None, timeout=TIMEOUT, no_verify_ssl=False, **kwargs):
        
        self.logger = logger
        self.remote = remote
        self.token = str(token)
        self.proxy = proxy
        self.timeout = timeout

        if no_verify_ssl:
            self.verify_ssl = False
        else:
            self.verify_ssl = True
        
        self.session = requests.session()
        self.session.headers["Accept"] = 'application/vnd.wf.v' + str(API_VERSION) + 'json'
        self.session.headers['User-Agent'] = 'whiteface-sdk-python/' + whiteface.sdk.VERSION
        self.session.headers['Authorization'] = 'Token token=' + self.token
        self.session.headers['Content-Type'] = 'application/json'

    def get(self, uri, params={}):
        body = self.session.get(uri, params=params, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            self.logger.debug(err)
            try:
                err = json.loads(body.content).get('message')
            except ValueError as e:
                err = body.content

            self.logger.error(err)
            raise RuntimeWarning(err)


        body = json.loads(body.content)
        return body

    def post(self, uri, data):
        data = json.dumps(data)

        body = self.session.post(uri, data=data, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            self.logger.debug(err)
            err = body.content

            if body.status_code == 401:
                err = 'unauthroized'
                raise RuntimeError(err)
            elif body.status_code == 404:
                err = 'not found'
                raise RuntimeError(err)
            else:
                try:
                    err = json.loads(err).get('message')
                except ValueError as e:
                    err = body.content

                self.logger.error(err)
                raise RuntimeWarning(err)

        body = json.loads(body.content)
        return body

    def ping(self):
        t0 = time.time()
        uri = str(self.remote)

        body = self.get(uri)

        t1 = (time.time() - t0)
        self.logger.debug('return time: %.15f' % t1)
        return t1

    def feed(self, user, feed):
        uri = self.remote + '/users/{0}/feeds/{1}'.format(user, feed)

        body = self.get(uri)
        return body['feed']['observables']

    def feed_create(self, user, name):
        uri = self.remote + '/users/{0}/feeds'.format(user)

        data = {
            'feed': {
                'name': name
            }
        }

        body = self.post(uri, data)
        if body.get('feed'):
            return body['feed']

        return body

    def observable(self, thing, user=None, feed=None):
        uri = self.remote + '/search'

        if user:
            uri = '/{0}/users/{1}'.format(uri, user)

        if feed:
            uri = '{0}/feeds/{1}'.format(uri, feed)

        uri = '{0}?q={1}'.format(uri, thing)

        self.logger.debug(uri)

        body = self.get(uri)
        return body

    def observable_create(self, user, feed, thing, tags=[], comment=None):
        if not user:
            raise RuntimeError('missing user name')

        if not feed:
            raise RuntimeError('missing feed name')

        uri = self.remote + '/users/{0}/feeds/{1}/observables'.format(user, feed)

        data = {
            "observable": {
                "thing": thing,
            },
            "tags": tags,
            "comment": comment
        }

        data = self.post(uri, data)
        return data