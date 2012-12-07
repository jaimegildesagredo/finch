# -*- coding: utf-8 -*-

from tornado import httpclient, ioloop, escape

from finch import *


class Repos(Collection):
    url = 'https://api.github.com/users/jaimegildesagredo/repos'

    def parse(self, body, headers):
        raw = escape.json_decode(body)

        return [parse_repo(r) for r in raw]

    class model(Model):
        id = IntegerField()
        name = StringField()
        owner = StringField()
        private = BoolField()

        def parse(self, body, headers):
            return parse_repo(escape.json_decode(body))


def parse_repo(raw):
    return {
        'id': raw['id'],
        'name': raw['name'],
        'owner': raw['owner']['login'],
        'private': raw['private']
    }


if __name__ == '__main__':
    repositories = Repos(httpclient.AsyncHTTPClient())

    def on_repos(repos, error):
        ioloop.IOLoop.instance().stop()

        if error:
            print 'Error fetching repos.'
            raise error

        for repo in repos:
            print repo.id, repo.name

    repositories.all(on_repos)
    ioloop.IOLoop.instance().start()
