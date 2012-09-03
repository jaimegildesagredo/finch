# -*- coding: utf-8 -*-

import httplib

from tornado import escape

import booby


class Session(object):
    def __init__(self, endpoint, client):
        self.endpoint = endpoint
        self.client = client

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

        self.client.fetch(self.url(model), callback=on_response)

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

        self.client.fetch(self.url(model, id_), callback=on_response)

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

        self.client.fetch(self.url(model), method='POST',
            body=escape.json_encode(dict(model)), callback=on_response)

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
