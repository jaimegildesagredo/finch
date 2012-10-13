# -*- coding: utf-8 -*-

from tornado import httpclient

from finch import Session


def before_all(context):
    context.session = Session(httpclient.AsyncHTTPClient())
    context.authenticated = False
