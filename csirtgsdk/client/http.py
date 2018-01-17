import json
import requests
import logging
from csirtgsdk.exceptions import AuthError, TimeoutError, NotFound, SubmissionFailed, RateLimitExceeded, SystemBusy
import os
import random
from time import sleep
from csirtgsdk import VERSION
from csirtgsdk.constants import API_VERSION, TIMEOUT, REMOTE, LIMIT, TOKEN
import gzip

RETRIES = os.getenv('CSIRTGSDK_CLIENT_HTTP_RETRIES', 5)
RETRIES_DELAY = os.getenv('CSIRTGSDK_CLIENT_HTTP_RETRIES_DELAY', '30,60')

s, e = RETRIES_DELAY.split(',')
RETRIES_DELAY = random.uniform(int(s), int(e))

logger = logging.getLogger(__name__)

if os.getenv('CSIRTGSDK_HTTP_TRACE'):
    logger.setLevel(logging.DEBUG)


class HTTP(object):
    def __init__(self, remote=REMOTE, token=TOKEN, proxy=None, timeout=TIMEOUT, verify_ssl=True):

        self.logger = logger
        self.remote = remote
        self.token = str(token)
        self.proxy = proxy
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.verify_ssl:
            self.logger.debug('TLS Verification is OFF')

        self.session = requests.session()
        self.session.headers["Accept"] = 'application/vnd.csirtg.v{0}'.format(str(API_VERSION))
        self.session.headers['User-Agent'] = 'csirtgsdk-python/{0}'.format(VERSION)
        self.session.headers['Authorization'] = 'Token token=' + self.token
        self.session.headers['Content-Type'] = 'application/json'
        self.session.headers['Accept-Encoding'] = 'gzip'

        #self.logger.debug(self.session.headers)

    def _check_return(self, resp, expects=[200, 201]):
        if isinstance(expects, int):
            expects = [expects]

        if resp.status_code in expects:
            return True

        if resp.status_code == 401:
            raise AuthError()

        if resp.status_code == 404:
            raise NotFound()

        if resp.status_code == 408:
            raise TimeoutError()

        if resp.status_code == 422:
            raise SubmissionFailed()

        if resp.status_code == 429:
            raise RateLimitExceeded()

        if resp.status_code in [500, 501, 502, 503, 504]:
            raise SystemBusy()

        raise RuntimeError(resp.text)

    def _get(self, uri, params={}):
        """
        HTTP GET function

        :param uri: REST endpoint
        :param params: optional HTTP params to pass to the endpoint
        :return: list of results (usually a list of dicts)

        Example:
            ret = cli.get('/search', params={ 'q': 'example.org' })
        """

        if not uri.startswith(self.remote):
            uri = '{}{}'.format(self.remote, uri)

        self.logger.debug(uri)

        resp = self.session.get(uri, params=params, verify=self.verify_ssl)

        self._check_return(resp)
        self.logger.debug(resp.headers)
        return json.loads(resp.text)

    get = _get

    def _post(self, uri, data):
        """
        HTTP POST function

        :param uri: REST endpoint to POST to
        :param data: list of dicts to be passed to the endpoint
        :return: list of dicts, usually will be a list of objects or id's

        Example:
            ret = cli.post('/indicators', { 'indicator': 'example.com' })
        """

        if not uri.startswith(self.remote):  # append self.remote if the uri doesn't include it
            uri = '{}/{}'.format(self.remote, uri)
            self.logger.debug(uri)

        data = json.dumps(data)

        resp = self.session.post(uri, data=data, verify=self.verify_ssl)

        n = RETRIES
        try:
            self._check_return(resp)
            n = 0
        except Exception as e:
            logger.error(e)
            if resp.status_code not in [500, 501, 502, 503, 504]:
                raise e

        while n != 0:
            logger.info('setting random retry interval to spread out the load')
            logger.info('retrying in %.00fs' % RETRIES_DELAY)
            sleep(RETRIES_DELAY)

            resp = self.session.post(uri, data=data, verify=self.verify_ssl)
            if self._check_return(resp):
                break

            if n == 0:
                raise SystemBusy('system seems busy.. try again later')

        return json.loads(resp.text)

    post = _post