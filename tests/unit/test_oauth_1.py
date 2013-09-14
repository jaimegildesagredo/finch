# -*- coding: utf-8 -*-

from hamcrest import *
from tornado import httpclient

from finch.auth import OAuth1

CLIENT_KEY = u'rktPBGeYBI'
RESOURCE_OWNER_KEY = u'9jI0xz9jdg'


class TestOAuth1(object):
    def test_when_auth_then_returns_request_with_authorization_header(self):
        auth = OAuth1(
            client_key=CLIENT_KEY,
            client_secret=u'QHhc2jgDEMngbbnPPmtM',
            resource_owner_key=RESOURCE_OWNER_KEY,
            resource_owner_secret=u'4VqKRi3hL9g0Ol3qnVR7'
        )

        request = httpclient.HTTPRequest('http://example.com/test')

        auth(request)

        assert_that(request.headers, has_entry('Authorization', all_of(
            contains_string('oauth_nonce="'),
            contains_string('oauth_timestamp="'),
            contains_string('oauth_version="1.0"'),
            contains_string('oauth_signature_method="HMAC-SHA1"'),
            contains_string('oauth_consumer_key="{}"'.format(CLIENT_KEY)),
            contains_string('oauth_token="{}"'.format(RESOURCE_OWNER_KEY)),
            contains_string('oauth_signature="')
        )))
