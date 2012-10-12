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

import httplib
import logging

from tornado import escape

from booby import Model, EmbeddedModel, IntegerField, StringField, BoolField


class Session(object):
    def __init__(self, endpoint, client):
        self.endpoint = endpoint
        self.client = client
        self.logger = logging.getLogger('finch.session')

    def all(self, model, callback):
        def on_response(response):
            if response.code >= httplib.BAD_REQUEST:
                callback(collection=None, error=SessionError(httplib.responses[response.code]))
                return

            collection = escape.json_decode(response.body)
            if hasattr(model._collection, 'parse'):
                collection = model._collection.parse(collection)

            try:
                result = []
                for raw in collection:
                    r = model()
                    r.update(r.parse(raw))
                    result.append(r)
            except ValueError as error:
                result = None
            else:
                error = None
            finally:
                callback(collection=result, error=error)

        url = self.url(model)
        self.client.fetch(url, callback=on_response)
        self.logger.info('GET {0}'.format(url))

    def get(self, model, id_, callback):
        def on_response(response):
            if response.code >= httplib.BAD_REQUEST:
                callback(model=None, error=SessionError(httplib.responses[response.code]))
                return

            result = model()

            try:
                result.update(result.parse(escape.json_decode(response.body)))
            except ValueError as error:
                result = None
            else:
                error = None
            finally:
                callback(model=result, error=error)

        url = self.url(model, id_)
        self.client.fetch(url, callback=on_response)
        self.logger.info('GET {0}'.format(url))

    def add(self, model, callback):
        def on_response(response):
            if response.code >= httplib.BAD_REQUEST:
                callback(model=None, error=SessionError(httplib.responses[response.code]))
                return

            result = model

            try:
                result.update(result.parse(escape.json_decode(response.body)))
            except ValueError as error:
                result = None
            else:
                error = None

            callback(model=result, error=error)

        url = self.url(model)
        self.client.fetch(url, method='POST',
            body=escape.json_encode(model.to_dict()), callback=on_response)

        self.logger.info('POST {0}'.format(url))

    def url(self, model, id_=None):
        result = self.endpoint + '/'

        if isinstance(model._collection, Collection):
            result += model._collection.url
        else:
            result += model._collection

        if id_ is not None:
            result += '/' + str(id_)
        return result


class SessionError(Exception):
    pass


class Resource(Model):
    def parse(self, raw):
        return raw


class Collection(object):
    model = None

    def __init__(self, client):
        self.client = client

    def all(self, callback):
        def on_response(response):
            if response.code >= httplib.BAD_REQUEST:
                callback(None, HTTPError(response.code))
                return

            # Get raw collection response
            raw_collection = escape.json_decode(response.body)
            if hasattr(self, 'parse'):
                raw_collection = self.parse(raw_collection)

            if not isinstance(raw_collection, list):
                callback(None, ValueError("""
                    Response content should be a list.
                    Overwrite the Collection.parse method to create a valid response.
                    """))
                return

            result = []
            try:
                # Build each model from the raw collection
                for raw in raw_collection:
                    r = self.model()
                    if hasattr(r, 'parse'):
                        r.update(r.parse(raw))
                    else:
                        r.update(raw)
                    result.append(r)
            except ValueError as error:
                # booby.Model error
                callback(None, error)
                return
            callback(result, None)

        self.client.fetch(self.url, callback=on_response)

    def get(self, id_, callback):
        def on_response(response):
            if response.code >= httplib.BAD_REQUEST:
                callback(None, HTTPError(response.code))
                return

            raw = escape.json_decode(response.body)

            result = self.model()
            try:
                if hasattr(result, 'parse'):
                    result.update(result.parse(raw))
                else:
                    result.update(raw)
            except ValueError as error:
                # booby.Model error
                callback(None, error)
                return

            callback(result, None)

        self.client.fetch('{0}/{1}'.format(self.url, id_), callback=on_response)

    def add(self, obj, callback):
        def on_response(response):
            if response.code >= httplib.BAD_REQUEST:
                callback(None, HTTPError(response.code))
                return

            raw = escape.json_decode(response.body)

            try:
                if hasattr(obj, 'parse'):
                    obj.update(obj.parse(raw))
                else:
                    obj.update(raw)
            except ValueError as error:
                callback(None, error)
                return

            callback(obj, None)

        self.client.fetch(self.url, method='POST', callback=on_response)


class HTTPError(Exception):
    def __init__(self, code):
        super(HTTPError, self).__init__(httplib.responses[code])
        self.code = code


class CollectionError(Exception):
    pass


__all__ = ['Resource', 'Model', 'Collection', 'Session', 'SessionError',
    'EmbeddedModel', 'IntegerField', 'StringField', 'BoolField']
