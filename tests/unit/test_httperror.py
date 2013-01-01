# -*- coding: utf-8 -*-

import httplib

from hamcrest import *

from finch import errors


class TestHTTPError(object):
    def test_when_404_then_message_is_not_found(self):
        http_error = errors.HTTPError(404)

        assert_that(http_error.message, is_(httplib.responses[404]))
        assert_that(http_error.code, is_(404))

    def test_when_599_then_message_is_timeout(self):
        http_error = errors.HTTPError(599)

        assert_that(http_error.message, is_('Timeout'))
        assert_that(http_error.code, is_(599))
