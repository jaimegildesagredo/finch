# -*- coding: utf-8 -*-

from tornado import httpclient
from hamcrest import *
from doublex import *

from finch import Session


class TestSession(object):
    def test_when_fetch_then_calls_http_client_fetch_with_the_same_args(self):
        with Spy(httpclient.HTTPClient()) as http_client:
            session = Session(http_client)

        callback = Stub()

        session.fetch('/users', method='POST', callback=callback,
            headers={'Content-Type': 'application/json'})

        assert_that(http_client.fetch, called().with_args(
            '/users', method='POST', callback=callback,
                headers={'Content-Type': 'application/json'})
            )


class TestSessionWithBasicAuth(object):
    def test_when_fetch_then_perform_request_with_basic_auth(self):
        with Spy(httpclient.HTTPClient()) as http_client:
            session = Session(http_client, auth=('root', 'toor'))

        session.fetch('/users')

        assert_that(http_client.fetch, called().with_args('/users',
            headers=has_entry('Authorization', 'Basic cm9vdDp0b29y')))

    def test_when_fetch_only_with_an_username_then_perform_request_with_basic_auth(self):
        with Spy(httpclient.HTTPClient()) as http_client:
            session = Session(http_client, auth=('root',))

        session.fetch('/users')

        assert_that(http_client.fetch, called().with_args('/users',
            headers=has_entry('Authorization', 'Basic cm9vdDo=')))
