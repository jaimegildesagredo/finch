# -*- coding: utf-8 -*-

from tornado import escape

import booby


class Session(object):
    def __init__(self, endpoint, client):
        self.endpoint = endpoint
        self.client = client

    def get(self, model, id_, callback):
        def on_response(response):
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
            model.update(escape.json_decode(response.body))
            callback(model)

        self.client.fetch(self.url(model), method='POST',
            body=escape.json_encode(dict(model)), callback=on_response)

    def url(self, model, id_=None):
        result = self.endpoint + '/' + model._collection
        if id_ is not None:
            result += '/' + str(id_)
        return result


class Resource(booby.Model):
    def parse(self, raw):
        return raw
