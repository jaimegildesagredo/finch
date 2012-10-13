# -*- coding: utf-8 -*-

from tornado import httpclient

from finch import Collection
from booby import Model, IntegerField, StringField


class Users(Collection):
    class model(Model):
        id = IntegerField()
        name = StringField()

    url = 'http://localhost:3000/users'


def before_all(context):
    context.collection = Users(httpclient.AsyncHTTPClient())
