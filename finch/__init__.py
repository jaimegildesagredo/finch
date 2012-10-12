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

from tornado import escape

from booby import Model, EmbeddedModel, IntegerField, StringField, BoolField


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


__all__ = ['Collection', 'Model', 'EmbeddedModel', 'IntegerField',
    'StringField', 'BoolField', 'HTTPError']
