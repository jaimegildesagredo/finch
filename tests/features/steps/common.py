# -*- coding: utf-8 -*-

from behave import given
from tornado import httpclient

from finch import Session, Collection
from booby import Model, fields


class Users(Collection):
    class model(Model):
        id = fields.Integer()
        name = fields.String()

    url = 'http://localhost:3000/users'


@given(u'I have the users collection')
def impl(context):
    context.collection = Users(context.session)


@given(u'I have an authenticated session')
def impl(context):
    context.session = Session(httpclient.AsyncHTTPClient(),
        auth=('admin', 'admin'))


@given(u'the collection is authenticated')
def impl(context):
    context.collection.url += '?auth=1'
