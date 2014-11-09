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

try:
    from http.client import BAD_REQUEST
except ImportError:
    from httplib import BAD_REQUEST
try:
    from urllib.parse import splitquery
except ImportError:
    from urllib import splitquery

from functools import partial

import booby.inspection
from tornado import escape

from finch import errors


class Collection(object):
    model = None

    def __init__(self, client):
        self.client = client

    def on_error(self, callback, response):
        callback(errors.HTTPError(response.code))

    def all(self, callback):
        self.request_all(callback)

    def request_all(self, callback):
        self.client.fetch(self.url, callback=partial(self.on_query, callback))

    def query(self, params, callback):
        self.request_query(callback, params)

    def request_query(self, params, callback):
        self.client.fetch(self.url, params=params, callback=partial(self.on_query, callback))

    def on_query(self, callback, response):
        if response.code >= BAD_REQUEST:
            self.on_error(partial(callback, None), response)
            return

        if hasattr(self, 'decode'):
            collection = self.decode(response)
        else:
            collection = escape.json_decode(response.body)

        if not isinstance(collection, list):
            callback(None, ValueError("""
                The response body was expected to be a JSON array.

                To properly process the response you should define a
                `decode(response)` method in your `Collection` class."""))

            return

        result = []

        try:
            for r in collection:
                obj = self.model(**r)
                obj._persisted = True
                result.append(obj)
        except Exception as error:
            callback(None, error)
        else:
            callback(result, None)

    def get(self, id_, callback):
        self.request_get(id_, callback)

    def request_get(self, id_, callback):
        self.client.fetch(self._url(id_), callback=partial(self.on_get, callback))

    def on_get(self, callback, response):
        if response.code >= BAD_REQUEST:
            self.on_error(partial(callback, None), response)
            return

        result = self.model()

        if hasattr(result, 'decode'):
            resource = result.decode(response)
        else:
            resource = escape.json_decode(response.body)

        try:
            result.update(resource)
        except Exception as error:
            callback(None, error)
        else:
            result._persisted = True
            callback(result, None)

    def _url(self, obj_or_id):
        if isinstance(obj_or_id, self.model):
            id_ = self._id(obj_or_id)
            url = getattr(obj_or_id, '_url', self.url)
        else:
            id_ = obj_or_id
            url = getattr(self.model, '_url', self.url)

        if callable(url):
            return url(id_)

        url, query = splitquery(url)

        url = '{}/{}'.format(url, id_)

        if query is not None:
            url = '{}?{}'.format(url, query)

        return url

    def add(self, obj, callback):
        self.request_add(obj, callback)

    def request_add(self, obj, callback):
        if getattr(obj, '_persisted', False) is True:
            url = self._url(obj)
            method = 'PUT'
        else:
            url = self.url
            method = 'POST'

        if hasattr(obj, 'encode'):
            body, content_type = obj.encode()
        else:
            body, content_type = escape.json_encode(dict(obj)), 'application/json'

        self.client.fetch(
            url,
            method=method,
            headers={'Content-Type': content_type},
            body=body,
            callback=partial(self.on_add, callback, obj))

    def _id(self, obj):
        for name, field in booby.inspection.get_fields(obj).items():
            if field.options.get('primary', False):
                return getattr(obj, name)

    def on_add(self, callback, obj, response):
        if response.code >= BAD_REQUEST:
            self.on_error(partial(callback, None), response)
            return

        try:
            obj._url = response.headers['Location']
        except KeyError:
            pass

        if len(response.body) == 0:
            obj._persisted = True
            callback(obj, None)
        else:
            if hasattr(obj, 'decode'):
                resource = obj.decode(response)
            else:
                resource = escape.json_decode(response.body)

            try:
                obj.update(resource)
            except Exception as error:
                callback(None, error)
            else:
                obj._persisted = True
                callback(obj, None)

    def delete(self, obj, callback):
        self.request_delete(obj, callback)

    def request_delete(self, obj, callback):
        self.client.fetch(
            self._url(obj),
            method='DELETE',
            callback=partial(self.on_delete, callback))

    def on_delete(self, callback, response):
        if response.code >= BAD_REQUEST:
            self.on_error(callback, response)
            return

        callback(None)
