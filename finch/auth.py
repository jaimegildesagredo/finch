# -*- coding: utf-8 -*-

import base64
import sys

from oauthlib.oauth1 import rfc5849

if sys.version > "3":
    unicode = str

class HTTPBasicAuth(object):
    def __init__(self, username, password=None):
        self.username = username
        self.password = password

    def __call__(self, request):
        request.headers['Authorization'] = _basic_auth_str(self.username, self.password)


def _basic_auth_str(username, password=None):
    auth = '{0}:'.format(username)

    if password is not None:
        auth += '{0}'.format(password)

    try:
        auth = bytes(auth, "utf-8")
    except TypeError:  # python 2
        pass

    return b'Basic ' + base64.b64encode(auth)


class OAuth1(object):
    def __init__(self, client_key, client_secret, resource_owner_key, resource_owner_secret):
        self._oauth_client = rfc5849.Client(
            client_key=client_key,
            client_secret=client_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret
        )

    def __call__(self, request):
        request.url, request.headers, request.body = self._oauth_client.sign(
            unicode(request.url),
            unicode(request.method),
            request.body,
            request.headers
        )
