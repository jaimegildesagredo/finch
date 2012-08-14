# -*- coding: utf-8 -*-

import httplib

from tornado import testing, escape

import finch
import booby


class TestSession(testing.AsyncTestCase):
    def test_get_success_runs_callback_with_model(self):
        client = FakeHTTPClient()
        client.response = httplib.OK, escape.json_encode({
            'id': 2,
            'name': 'Jack',
            'email': 'jack@example.com'
        })

        session = finch.Session('http://example.com/api', client=client)

        session.get(User, 2, self.stop)
        user = self.wait()

        self.assertEqual(user.id, 2)
        self.assertEqual(user.name, 'Jack')
        self.assertEqual(user.email, 'jack@example.com')


class FakeHTTPClient(object):
    def __init__(self):
        self._response = None

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = FakeHTTPResponse(*value)

    def fetch(self, request, callback, **kwargs):
        callback(self.response)


class FakeHTTPResponse(object):
    def __init__(self, code, body):
        self.code = code
        self.body = body


class User(booby.Model):
    _collection = 'users'

    id = booby.IntegerField(primary=True)
    name = booby.StringField()
    email = booby.StringField()
