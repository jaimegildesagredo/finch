# -*- coding: utf-8 -*-

from tornado import escape


class Session(object):
    def __init__(self, endpoint, client):
        self.endpoint = endpoint
        self.client = client

    def get(self, model, id_, callback):
        def on_response(response):
            if hasattr(model, 'parse'):
                result = model.parse(escape.json_decode(response.body))
            else:
                result = model(**escape.json_decode(response.body))

            callback(result)

        self.client.fetch(self.url(model, id_), callback=on_response)

    def url(self, model, id_):
        return self.endpoint + '/' + model._collection + '/' + str(id_)
