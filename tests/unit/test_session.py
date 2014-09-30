# -*- coding: utf-8 -*-

from tornado import httpclient
from hamcrest import *
from doublex import *

from finch import Session, auth


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

    def test_when_fetch_with_params_then_calls_http_client_fetch_with_params_added_to_url(self):
        with Spy(httpclient.HTTPClient()) as http_client:
            session = Session(http_client)

        session.fetch('/users?type=json', callback=CALLBACK, params={'is_admin': 'true'})

        assert_that(http_client.fetch, called().with_args(
            has_properties(
                url='/users?type=json&is_admin=true'
            ),
            callback=CALLBACK
        ))

    def test_when_base_url_set_then_calls_http_client_fetch_with_base_url(self):
        with Spy(httpclient.HTTPClient()) as http_client:
            session = Session(http_client, base_url='https://example.com:12345')

        session.fetch('/users?type=json', callback=CALLBACK, params={'is_admin': 'true'})

        assert_that(http_client.fetch, called().with_args(
            has_properties(
                url='https://example.com:12345/users?type=json&is_admin=true'
            ),
            callback=CALLBACK
        ))

class TestSessionWithBasicAuth(object):
    def test_when_auth_is_username_and_password_tuple_then_session_uses_basic_auth(self):
        session = Session(Stub(), auth=(u'root', u'toor'))

        assert_that(session.auth, instance_of(auth.HTTPBasicAuth))
        assert_that(session.auth, has_properties(
            username=u'root', password=u'toor'))

    def test_when_auth_is_username_tuple_then_session_uses_basic_auth(self):
        session = Session(Stub(), auth=(u'root',))

        assert_that(session.auth, instance_of(auth.HTTPBasicAuth))
        assert_that(session.auth, has_properties(
            username=u'root', password=None))


class TestSessionWithAuth(object):
    def test_when_fetch_then_performs_auth(self):
        auth = Spy().auth

        session = Session(Stub(), auth=auth)

        session.fetch('/users', callback=CALLBACK)

        assert_that(auth, called().with_args(instance_of(httpclient.HTTPRequest)))
