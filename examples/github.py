# -*- coding: utf-8 -*-

from tornado import httpclient, ioloop

from finch import *


class Repos(Collection):
    url = 'https://api.github.com/users/jaimegildesagredo/repos'

    class model(Model):
        id = IntegerField()
        name = StringField()
        owner = StringField()
        private = BoolField()

        def parse(self, raw):
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
