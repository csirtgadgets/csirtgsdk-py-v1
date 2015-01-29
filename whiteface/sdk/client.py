import json
import requests
import time
import logging
import whiteface.sdk

import pprint
pp = pprint.PrettyPrinter()

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

    def search(self,limit=LIMIT,nolog=None,filters={},sort='lasttime'):
        filters['limit'] = limit
        filters['nolog'] = nolog
        
        uri = self.remote + '/observables'
            
        self.logger.debug('uri: %s' % uri)
        self.logger.debug('params: %s', json.dumps(filters))
        
        body = self.session.get(uri, params=filters, verify=self.verify_ssl)
        
        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)
        
        body = json.loads(body.text)
        body = sorted(body, key=lambda o: o[sort])
        return body

    def submit(self, feed=None, data=None, user=None):
        '''
        '{"observable":"example.com","confidence":"50",":tlp":"amber",
        "provider":"me.com","tags":["zeus","botnet"]}'
        '''
        if not data:
            return None
        
        # TODO - http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
        uri = self.remote + '/users/{0}/feeds/{1}/observables'.format(user, feed)
        
        self.logger.debug('uri: %s' % uri)

        data = json.dumps(data)
         
        body = self.session.post(uri,data=data, verify=self.verify_ssl)

        self.logger.debug('status code: ' + str(body.status_code))

        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            self.logger.error(json.loads(body.content).get('message'))
            return None
        
        body = json.loads(body.content)
        return body

    def ping(self):
        t0 = time.time()
        uri = str(self.remote)
        body = self.session.get(uri,params={}, verify=self.verify_ssl)

        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            self.logger.error('request failed: %s' % str(body.status_code))
            return 'request failed: %s' % str(body.status_code)

        t1 = (time.time() - t0)
        self.logger.debug('return time: %.15f' % t1)
        return t1

    def feed(self, user, feed):
        uri = self.remote + '/users/{0}/feeds/{1}'.format(user, feed)

        body = self.session.get(uri, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            self.logger.debug(err)
            self.logger.debug(json.loads(body.content).get('message'))
            raise RuntimeWarning(err)

        body = json.loads(body.content)
        return body['feed']['observables']

    def feed_create(self, user, name):
        uri = self.remote + '/users/{0}/feeds'.format(user)

        data = {
            'feed': {
                'name': name
            }
        }

        data = json.dumps(data)

        body = self.session.post(uri, data=data, verify=self.verify_ssl)

        if body.status_code > 303:
            err = 'request failed: %s' % str(body.status_code)
            self.logger.debug(err)
            self.logger.debug(json.loads(body.content).get('message'))
            raise RuntimeWarning(err)

        self.logger.info('feed already exists...')
        body = json.loads(body.content)
        return body

    def observable(self, thing, user=None, feed=None):
        uri = self.remote + '/search'

        if user:
            uri = uri + '/{0}/users/{1}'.format(uri, user)

        if feed:
            uri = '{0}/feeds/{1}'.format(uri, feed)

        uri = '{0}?q={1}'.format(uri, thing)

        self.logger.debug(uri)

        body = self.session.get(uri, params={}, verify=self.verify_ssl)

        self.logger.debug('status code: ' + str(body.status_code))
        if body.status_code > 299:
            raise RuntimeError('request failed: %s' % str(body.status_code))

        return json.loads(body.content)

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

        data = json.dumps(data)

        ret = self.session.post(uri, data=data, verify=self.verify_ssl)

        if ret.status_code > 299:
            err = 'request failed: %s' % str(ret.status_code)
            raise RuntimeWarning(err)

        return json.loads(ret.content)
