# -*- coding: utf-8 -*-

from tornado import escape


class Session(object):
    def __init__(self, endpoint, client):
        self.endpoint = endpoint
        self.client = client

    def get(self, model, id_, callback):
        def callback_(response):
            callback(model(**escape.json_decode(response.body)))

        self.client.fetch(self.url(model, id_), callback=callback_)

    def url(self, model, id_):
        return self.endpoint + '/' + model._collection + '/' + str(id_)
