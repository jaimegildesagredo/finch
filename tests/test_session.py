# -*- coding: utf-8 -*-

import httplib

from tornado import testing, escape

import finch
import booby


class TestSession(testing.AsyncTestCase):
    URL = 'http://example.com/api'

    def test_get_success_runs_callback_with_model(self):
        self.client.response = httplib.OK, escape.json_encode({
            'id': 2,
            'name': 'Jack',
            'email': 'jack@example.com'
        })

        self.session.get(User, 2, self.stop)
        user = self.wait()

        self.assertEqual(user.id, 2)
        self.assertEqual(user.name, 'Jack')
        self.assertEqual(user.email, 'jack@example.com')

    def test_get_gets_model_from_collection(self):
        self.client.response = httplib.OK, escape.json_encode({
            'id': 2,
            'name': 'Jack',
            'email': 'jack@example.com'
        })

        self.session.get(User, 2, self.stop)
        self.wait()

        self.assertEqual(self.client.last_request.url, self.URL + '/users/2')
        self.assertEqual(self.client.last_request.method, 'GET')

    def test_add_success_runs_callback_with_model(self):
        self.client.response = httplib.CREATED, escape.json_encode({
            'id': 2,
            'name': 'Jack',
            'email': 'jack@example.com'
        })

        user = User(name='Jack', email='jack@example.com')

        self.session.add(user, self.stop)

        self.assertEqual(user, self.wait())
        self.assertEqual(user.id, 2)

    def test_add_post_model_to_collection(self):
        self.client.response = httplib.CREATED, escape.json_encode({
            'id': 2,
            'name': 'Jack',
            'email': 'jack@example.com'
        })

        user = User(name='Jack', email='jack@example.com')

        self.session.add(user, self.stop)
        self.wait()

        self.assertEqual(self.client.last_request.url, self.URL + '/users')
        self.assertEqual(self.client.last_request.method, 'POST')
        self.assertEqual(self.client.last_request.body,
            '{"id": null, "name": "Jack", "email": "jack@example.com"}')

    def setUp(self):
        super(TestSession, self).setUp()

        self.client = FakeHTTPClient()
        self.session = finch.Session(self.URL, client=self.client)


class FakeHTTPClient(object):
    def __init__(self):
        self._response = None
        self._last_request = None

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = FakeHTTPResponse(*value)

    @property
    def last_request(self):
        return self._last_request

    @last_request.setter
    def last_request(self, value):
        self._last_request = FakeHTTPRequest(*value)

    def fetch(self, request, callback, **kwargs):
        self.last_request = request, kwargs.get('method', 'GET'), kwargs.get('body')

        callback(self.response)


class FakeHTTPResponse(object):
    def __init__(self, code, body):
        self.code = code
        self.body = body


class FakeHTTPRequest(object):
    def __init__(self, url, method, body):
        self.url = url
        self.method = method
        self.body = body


class User(booby.Resource):
    _collection = 'users'

    id = booby.IntegerField()
    name = booby.StringField()
    email = booby.StringField()
