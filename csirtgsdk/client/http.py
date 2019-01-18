import json
import requests
import logging
from csirtgsdk.exceptions import AuthError, TimeoutError, NotFound, \
    SubmissionFailed, RateLimitExceeded, SystemBusy
import os
import random
from time import sleep

from csirtgsdk.constants import API_VERSION, TIMEOUT, REMOTE, TOKEN, \
    VERSION

RETRIES = os.getenv('CSIRTGSDK_CLIENT_HTTP_RETRIES', 5)
RETRIES_DELAY = os.getenv('CSIRTGSDK_CLIENT_HTTP_RETRIES_DELAY', '30,60')

s, e = RETRIES_DELAY.split(',')
RETRIES_DELAY = random.uniform(int(s), int(e))

logger = logging.getLogger(__name__)

if os.getenv('CSIRTGSDK_HTTP_TRACE'):
    logger.setLevel(logging.DEBUG)


class HTTP(object):
    def __init__(self, remote=REMOTE, token=TOKEN, proxy=None,
                 timeout=TIMEOUT, verify_ssl=True):

        self.logger = logger
        self.remote = remote
        self.token = str(token)
        self.proxy = proxy
        self.timeout = timeout
        self.verify_ssl = verify_ssl

        if not self.verify_ssl:
            self.logger.debug('TLS Verification is OFF')

        self.session = requests.session()
        self.session.headers["Accept"] = 'application/vnd.csirtg.v{0}'\
            .format(str(API_VERSION))
        self.session.headers['User-Agent'] = 'csirtgsdk-python/{0}'\
            .format(VERSION)
        self.session.headers['Authorization'] = 'Token token=' + self.token
        self.session.headers['Content-Type'] = 'application/json'
        self.session.headers['Accept-Encoding'] = 'gzip'

    @staticmethod
    def _check_return(resp, expects=[200, 201]):
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

    def _make_request(self, uri, params={}, data=None):
        n = 0
        while n != RETRIES:
            if len(params) > 0:
                resp = self.session.get(uri, params=params)
            else:
                resp = self.session.post(uri, data=json.dumps(data))

            try:
                self._check_return(resp)
                return json.loads(resp.text)

            except Exception as e:
                logger.error(e)
                if resp.status_code not in [500, 501, 502, 503, 504]:
                    raise e

            logger.info('random retrying in %.00fs' % RETRIES_DELAY)
            sleep(RETRIES_DELAY)

            n += 1

        if n == RETRIES:
            raise SystemBusy("Something went wrong, "
                             "check your data and/or try again later..")

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

        return self._make_request(uri, params)

    def _post(self, uri, data):
        """
        HTTP POST function

        :param uri: REST endpoint to POST to
        :param data: list of dicts to be passed to the endpoint
        :return: list of dicts, usually will be a list of objects or id's

        Example:
            ret = cli.post('/indicators', { 'indicator': 'example.com' })
        """

        if not uri.startswith(self.remote):
            uri = '{}/{}'.format(self.remote, uri)
            self.logger.debug(uri)

        return self._make_request(uri, data=data)

    post = _post
    get = _get
