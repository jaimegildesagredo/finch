# -*- coding: utf-8 -*-
#
# Copyright 2012 Jaime Gil de Sagredo Luna
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module is a wrapper on top of the Tornado's HTTPClient."""

import base64


class Session(object):
    def __init__(self, http_client, auth=None):
        self.http_client = http_client
        self.auth = auth

    def fetch(self, *args, **kwargs):
        if self.auth is not None:
            headers = kwargs.get('headers', {})
            if not headers:
                kwargs['headers'] = headers
            headers['Authorization'] = _basic_auth_str(*self.auth)

        self.http_client.fetch(*args, **kwargs)


def _basic_auth_str(username, password=None):
    auth = '{0}:'.format(username)

    if password is not None:
        auth += '{0}'.format(password)

    return 'Basic ' + base64.b64encode(auth)
