# -*- coding: utf-8 -*-

from tornado import httpclient, ioloop

import finch


class Repo(finch.Resource):
    _collection = 'users/jaimegildesagredo/repos'

    id = finch.IntegerField()
    name = finch.StringField()
    owner = finch.StringField()
    private = finch.BoolField()

    def parse(self, raw):
        return {
            'id': raw['id'],
            'name': raw['name'],
            'owner': raw['owner']['login'],
            'private': raw['private']
        }


if __name__ == '__main__':
    session = finch.Session('https://api.github.com', httpclient.AsyncHTTPClient())

    def on_repo(model, error):
        if error is None:
            print dict(model)
        else:
            print error.message
        ioloop.IOLoop.instance().stop()

    def on_repos(collection, error):
        if error is None:
            for repo in collection:
                print dict(repo)
        else:
            print error.message
        ioloop.IOLoop.instance().stop()

#    session.get(Repo, 'cormoran', on_repo)
    session.all(Repo, on_repos)
    ioloop.IOLoop.instance().start()
