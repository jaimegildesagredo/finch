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

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from tornado import httpclient
from tornado import httputil

from finch.auth import HTTPBasicAuth


class Session(object):
    def __init__(self, http_client, base_url=None, auth=None):
        self.http_client = http_client
        self.base_url = base_url

        if isinstance(auth, tuple):
            self.auth = HTTPBasicAuth(*auth)
        else:
            self.auth = auth

    def fetch(self, url, callback, params=None, **kwargs):
        if self.base_url is not None:
            url = urljoin(self.base_url, url)
        if params is not None:
            url = httputil.url_concat(url, params)

        request = httpclient.HTTPRequest(url=url, **kwargs)

        if self.auth is not None:
            self.auth(request)

        self.http_client.fetch(request, callback=callback)
