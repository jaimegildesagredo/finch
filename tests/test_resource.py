# -*- coding: utf-8 -*-

import unittest


import finch


class TestResource(unittest.TestCase):
    def test_parse_returns_passed_argument(self):
        resource = finch.Resource()
        raw_response = {'foo': 'bar'}

        self.assertEqual(resource.parse(raw_response), raw_response)
