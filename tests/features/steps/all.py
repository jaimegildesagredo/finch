# -*- coding: utf-8 -*-

from behave import when, then
from tornado import ioloop


@when(u'I get all the users')
def impl(context):
    def on_users(users, error):
        ioloop.IOLoop.instance().stop()
        context.users = users
        context.error = error

    context.collection.all(on_users)
    ioloop.IOLoop.instance().start()

    assert not context.error


@then(u'I should have a list of users')
def impl(context):
    assert isinstance(context.users, list)
    assert isinstance(context.users[0], context.collection.model)
