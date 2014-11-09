# -*- coding: utf-8 -*-

from hamcrest import *
from tornado import httpclient

from finch.auth import HTTPBasicAuth


class TestBasicAuth(object):
    def setup(self):
        self.auth = HTTPBasicAuth(u'root', u'toor')
        self.request = httpclient.HTTPRequest('/test')

    def test_when_auth_with_username_and_password_then_returns_request_with_authorization_header(self):
        self.auth(self.request)

        assert_that(self.request.headers,
            has_entry('Authorization', b'Basic cm9vdDp0b29y'))

    def test_when_auth_with_username_then_returns_request_with_authorization_header(self):
        self.auth = HTTPBasicAuth(u'root')

        self.auth(self.request)

        assert_that(self.request.headers,
            has_entry('Authorization', b'Basic cm9vdDo='))

    def test_when_auth_request_with_headers_then_returns_request_with_these_headers(self):
        self.request.headers = {'Content-Type': 'application/json'}

        self.auth(self.request)

        assert_that(self.request.headers,
            has_entry('Content-Type', 'application/json'))

    def test_when_auth_request_with_headers_then_returns_request_with_authorization_header(self):
        self.request.headers = {'Content-Type': 'application/json'}

        self.auth(self.request)

        assert_that(self.request.headers,
            has_entry('Authorization', b'Basic cm9vdDp0b29y'))
