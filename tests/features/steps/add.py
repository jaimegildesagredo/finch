# -*- coding: utf-8 -*-

from behave import given, when, then
from tornado import ioloop
from hamcrest import *


@given(u'I have the "{name}" user')
def impl(context, name):
    context.user = context.collection.model(name=name)


@when(u'I add it to the collection')
def impl(context):
    def on_added(user, error):
        ioloop.IOLoop.instance().stop()
        context.error = error

    context.collection.add(context.user, on_added)
    ioloop.IOLoop.instance().start()

    assert_that(context.error, is_(None))


@then(u'the user should have an id')
def impl(context):
    assert context.user.id is not None
