# -*- coding: utf-8 -*-


class HTTPClient(object):
    def __init__(self):
        self._next_response = None
        self._last_request = None

    @property
    def next_response(self):
        return self._next_response

    @next_response.setter
    def next_response(self, value):
        self._next_response = _HTTPResponse(*value)

    @property
    def last_request(self):
        return self._last_request

    @last_request.setter
    def last_request(self, value):
        self._last_request = _HTTPRequest(*value)

    def fetch(self, request, callback, **kwargs):
        self.last_request = request, kwargs

        callback(self.next_response)


class _HTTPResponse(object):
    def __init__(self, code, body, headers=None):
        self.code = code
        self.body = body

        if headers is None:
            headers = {}

        self.headers = headers


class _HTTPRequest(object):
    def __init__(self, url, options):
        self.url = url
        self.method = options.get('method', 'GET')
        self.body = options.get('body')
        self.headers = options.get('headers')
        self.params = options.get('params')
