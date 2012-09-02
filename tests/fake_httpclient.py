# -*- coding: utf-8 -*-


class HTTPClient(object):
    def __init__(self):
        self._response = None
        self._last_request = None

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = _HTTPResponse(*value)

    @property
    def last_request(self):
        return self._last_request

    @last_request.setter
    def last_request(self, value):
        self._last_request = _HTTPRequest(*value)

    def fetch(self, request, callback, **kwargs):
        self.last_request = request, kwargs.get('method', 'GET'), kwargs.get('body')

        callback(self.response)


class _HTTPResponse(object):
    def __init__(self, code, body):
        self.code = code
        self.body = body


class _HTTPRequest(object):
    def __init__(self, url, method, body):
        self.url = url
        self.method = method
        self.body = body
