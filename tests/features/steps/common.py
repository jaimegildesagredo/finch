# -*- coding: utf-8 -*-

from behave import given


@given(u'I have the users collection')
def impl(context):
    assert context.collection
