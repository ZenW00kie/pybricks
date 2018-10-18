import base64
import json
import warnings
import requests
import ssl
from requests.adapters import HTTPAdapter
try:
    from requests.packages.urllib3.poolmanager import PoolManager
    from requests.packages.urllib3 import exceptions
except ImportError:
    from urllib3.poolmanager import PoolManager
    from urllib3 import exceptions

from . import configure

class TlsV1HttpAdapter(HTTPAdapter):
    """
    A HTTP adapter implementation that specifies the ssl version to be TLS1.
    This avoids problems with openssl versions that
    use SSL3 as a default (which is not supported by the server side).
    """

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1_2)

class Session(object):

    def __init__(self,
                 host=None,
                 uname=None,
                 pwd=None,
                 token=None,
                 profile='DEFAULT'):
        self.session = requests.Session()
        self.session.mount('https://', TlsV1HttpAdapter())
        self.url = 'https://%s/api/2.0/' % host
        if uname and pwd:
            auth = {'Authorization':
                    'Basic ' + base64.standard_b64encode(
                        ('%s:%s' % (uname, pwd)).encode()).decode(),
                    'Content-Type': 'text/json'}
        elif token:
            auth = {'Authorization': 'Bearer %s' % token,
                    'Content-Type': 'text/json'}
        else:
            config = configure.get_config(profile)
            # Need prettier method given recursive class doesn't seem to work
            # Session(uname=config.username,
            #         pwd=config.password,
            #         token=config.token)
            uname=config.username
            pwd=config.password
            token=config.token
            if uname and pwd:
                auth = {'Authorization':
                        'Basic ' + base64.standard_b64encode(
                            ('%s:%s' % (uname, pwd)).encode()).decode(),
                        'Content-Type': 'text/json'}
            elif token:
                auth = {'Authorization': 'Bearer %s' % token,
                        'Content-Type': 'text/json'}
        user_agent = {'user-agent':'gdwn-sdk'}
        self.default_headers = {}
        self.default_headers.update(auth)
        self.default_headers.update(user_agent)

    def perform_query(self, method, path, data = {}, headers = None):
        """set up connection and perform query"""
        if headers is None:
            headers = self.default_headers

        with warnings.catch_warnings():
            warnings.simplefilter("ignore",
                                  exceptions.InsecureRequestWarning)
            resp = self.session.request(method,
                                        self.url + path,
                                        data = json.dumps(data),
                                        headers = headers)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
        return resp.json()
