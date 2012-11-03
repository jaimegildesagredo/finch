# -*- coding: utf-8 -*-

from hamcrest import *

from finch.auth import HTTPBasicAuth


class TestBasicAuth(object):
    def test_when_auth_with_username_and_password_then_returns_request_with_authorization_header(self):
        args, kwargs = self.auth((), {})

        assert_that(kwargs, has_entry('headers',
            has_entry('Authorization', 'Basic cm9vdDp0b29y')))

    def test_when_auth_with_username_then_returns_request_with_authorization_header(self):
        self.auth = HTTPBasicAuth(u'root')

        args, kwargs = self.auth((), {})

        assert_that(kwargs, has_entry('headers',
            has_entry('Authorization', 'Basic cm9vdDo=')))

    def test_when_auth_request_with_headers_then_returns_request_with_these_headers(self):
        args, kwargs = self.auth((), {'headers': {'Content-Type': 'application/json'}})

        assert_that(kwargs, has_entry('headers',
            has_entry('Content-Type', 'application/json')))

    def test_when_auth_request_with_headers_then_returns_request_with_authorization_header(self):
        args, kwargs = self.auth((), {'headers': {'Content-Type': 'application/json'}})

        assert_that(kwargs, has_entry('headers',
            has_entry('Authorization', 'Basic cm9vdDp0b29y')))

    def setup(self):
        self.auth = HTTPBasicAuth(u'root', u'toor')
