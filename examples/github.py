# -*- coding: utf-8 -*-

from tornado import httpclient, ioloop

import booby
import finch


class Repo(booby.Model):
    _collection = 'repos/jaimegildesagredo'

    id = booby.IntegerField()
    name = booby.StringField()
    owner = booby.StringField()
    private = booby.BoolField()

    @classmethod
    def parse(cls, raw):
        return cls(
            id=raw['id'],
            name=raw['name'],
            owner=raw['owner']['login'],
            private=raw['private'])


if __name__ == '__main__':
    session = finch.Session('https://api.github.com', httpclient.AsyncHTTPClient())

    def on_repo(model):
        print dict(model)
        ioloop.IOLoop.instance().stop()

    session.get(Repo, 'cormoran', on_repo)
    ioloop.IOLoop.instance().start()
