# -*- coding: utf-8 -*-

from tornado import httpclient
from hamcrest import *
from doublex import *

from finch import Session


class TestSession(object):
    def test_when_fetch_calls_http_client_fetch_with_the_same_args(self):
        with Spy(httpclient.HTTPClient()) as http_client:
            session = Session(http_client)

        callback = Stub()

        session.fetch('/users', method='POST', callback=callback,
            headers={'Content-Type': 'application/json'})

        assert_that(http_client.fetch, called().with_args(
            '/users', method='POST', callback=callback,
                headers={'Content-Type': 'application/json'})
            )
