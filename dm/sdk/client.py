import json
import requests
import time
import logging
import dm.sdk
from prettytable import PrettyTable

import pprint
pp = pprint.PrettyPrinter()

REMOTE ='https://dm.csirtgadgets.com/api'
LIMIT = 5000
TIMEOUT = 300

FORMAT_COLS = ['thing', 'portlist', 'application', 'tags', 'created_at']
MAX_FIELD_SIZE = 30

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
        self.session.headers["Accept"] = 'application/vnd.dm.v' + dm.sdk.__api_version__ + 'json'
        self.session.headers['User-Agent'] = 'dm-sdk-python/' + dm.sdk.__version__
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

    def table(self, data=[], cols=FORMAT_COLS):
        data = data['feed']['observables']

        t = PrettyTable(cols)

        for o in data:

            r = []
            for c in cols:
                y = o['observable'].get(c) or ''
                if type(y) is list:
                    y = ','.join(y)
                y = str(y)
                y = (y[:MAX_FIELD_SIZE] + '..') if len(y) > MAX_FIELD_SIZE else y
                r.append(y)
            t.add_row(r)
        return t



    def feed(self, user=None, feed=None):
        uri = self.remote + '/users/{0}/feeds/{1}'.format(user, feed)

        body = self.session.get(uri, verify=self.verify_ssl)

        return json.loads(body.content)
    
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
