import json
import requests
import logging
from csirtgsdk.exceptions import AuthError, TimeoutError, NotFound, SubmissionFailed, RateLimitExceeded
import os

from csirtgsdk import VERSION
from csirtgsdk.constants import API_VERSION, TIMEOUT, REMOTE, LIMIT, TOKEN
import gzip

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
        self.session.headers["Accept"] = 'application/vnd.csirtg.v{0}+json'.format(str(API_VERSION))
        self.session.headers['User-Agent'] = 'csirtgsdk-python/{0}'.format(VERSION)
        self.session.headers['Authorization'] = 'Token token=' + self.token
        self.session.headers['Content-Type'] = 'application/json'
        self.session.headers['Accept-Encoding'] = 'gzip'

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
        self._check_return(resp)
        return json.loads(resp.text)

    post = _post