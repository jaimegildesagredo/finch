# -*- coding: utf-8 -*-

from tornado import httpclient
from hamcrest import *
from doublex import *

from tests.matchers import has_properties

from finch import Session


CALLBACK = lambda: None


class TestSession(object):
    def test_when_fetch_then_calls_http_client_fetch_with_the_same_args(self):
        with Spy(httpclient.HTTPClient()) as http_client:
            session = Session(http_client)

        session.fetch('/users', method='POST', callback=CALLBACK,
            headers={'Content-Type': 'application/json'})

        assert_that(http_client.fetch, called().with_args(
            has_properties(
                url='/users',
                method='POST',
                headers={'Content-Type': 'application/json'}
            ),
            callback=CALLBACK
        ))


class TestSessionWithBasicAuth(object):
    def test_when_fetch_then_perform_request_with_basic_auth(self):
        with Spy(httpclient.HTTPClient()) as http_client:
            session = Session(http_client, auth=('root', 'toor'))

        session.fetch('/users', callback=CALLBACK)

        assert_that(http_client.fetch, called().with_args(
            has_properties(
                url='/users',
                headers=has_entry('Authorization', 'Basic cm9vdDp0b29y')
            ),
            ANY_ARG
        ))

    def test_when_fetch_only_with_an_username_then_perform_request_with_basic_auth(self):
        with Spy(httpclient.HTTPClient()) as http_client:
            session = Session(http_client, auth=('root',))

        session.fetch('/users', callback=CALLBACK)

        assert_that(http_client.fetch, called().with_args(
            has_properties(
                url='/users',
                headers=has_entry('Authorization', 'Basic cm9vdDo=')
            ),
            ANY_ARG
        ))
