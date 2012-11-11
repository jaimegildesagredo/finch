# -*- coding: utf-8 -*-

import base64


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

    return 'Basic ' + base64.b64encode(auth)
