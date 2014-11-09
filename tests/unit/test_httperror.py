# -*- coding: utf-8 -*-

try:
    from http.client import responses
except ImportError:
    from httplib import responses

from hamcrest import *

from finch import errors


class TestHTTPError(object):
    def test_when_404_then_message_is_not_found(self):
        http_error = errors.HTTPError(404)

        assert_that(str(http_error), is_(responses[404]))
        assert_that(http_error.code, is_(404))

    def test_when_422_then_message_is_default_message(self):
        http_error = errors.HTTPError(422)

        assert_that(str(http_error), is_('Status code 422'))

    def test_when_599_then_message_is_timeout(self):
        http_error = errors.HTTPError(599)

        assert_that(str(http_error), is_('Timeout'))
        assert_that(http_error.code, is_(599))
