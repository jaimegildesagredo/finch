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

import booby
from booby import EmbeddedModel, IntegerField, StringField, BoolField


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

            try:
                result = []
                for raw in escape.json_decode(response.body):
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
        result = self.endpoint + '/' + model._collection
        if id_ is not None:
            result += '/' + str(id_)
        return result


class SessionError(Exception):
    pass


class Resource(booby.Model):
    def parse(self, raw):
        return raw


__all__ = ['Resource', 'Session', 'SessionError', 'EmbeddedModel',
    'IntegerField', 'StringField', 'BoolField']
