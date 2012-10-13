# -*- coding: utf-8 -*-

from behave import when, then
from tornado import ioloop


@when(u'I get the user "{id_}"')
def impl(context, id_):
    def on_user(user, error):
        ioloop.IOLoop.instance().stop()
        context.user = user
        context.error = error

    context.collection.get(id_, on_user)
    ioloop.IOLoop.instance().start()

    assert not context.error


@then(u'I should have the user')
def impl(context):
    assert isinstance(context.user, context.collection.model)
