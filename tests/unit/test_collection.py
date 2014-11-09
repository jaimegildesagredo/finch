# -*- coding: utf-8 -*-

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from http.client import OK, NOT_FOUND, CREATED, NO_CONTENT, INTERNAL_SERVER_ERROR, BAD_REQUEST
except ImportError:
    from httplib import OK, NOT_FOUND, CREATED, NO_CONTENT, INTERNAL_SERVER_ERROR, BAD_REQUEST

import booby
from booby import Model, fields
from tornado import escape
from hamcrest import *

from tests.unit import AsyncTestCase, fake_httpclient

from finch import errors, Collection


class TestGetEntireCollection(AsyncTestCase):
    def test_when_response_is_a_json_array_then_runs_callback_with_collection(self):
        self.client.next_response = OK, self.json_collection

        self.collection.all(self.stop)
        users, error = self.wait()

        assert_that(not error)
        assert_that(users, contains(
            has_properties(id=1, name=u'Foo', email=u'foo@example.com'),
            has_properties(id=2, name=u'Jack', email=u'jack@example.com')
        ))

    def test_when_response_is_ok_then_runs_callback_with_persisted_objects_in_collection(self):
        self.client.next_response = OK, self.json_collection

        self.collection.all(self.stop)
        users, error = self.wait()

        assert_that(not error)
        assert_that(users, contains(
            has_property('_persisted', True),
            has_property('_persisted', True)))

    def test_when_response_is_not_a_json_array_and_collection_has_not_decode_method_then_runs_callback_with_error(self):
        self.json_collection = escape.json_encode({
            'users': [
                {
                    'id': 1,
                    'name': 'Foo',
                    'email': 'foo@example.com'
                },
                {
                    'id': 2,
                    'name': 'Jack',
                    'email': 'jack@example.com'
                }
            ]
        })

        self.client.next_response = OK, self.json_collection

        self.collection.all(self.stop)
        users, error = self.wait()

        assert_that(not users)
        assert_that(error, instance_of(ValueError))
        assert_that(str(error), contains_string(
            "The response body was expected to be a JSON array."))

    def test_when_response_resources_have_extra_fields_and_collection_has_not_decode_method_then_runs_callback_with_error(self):
        self.json_collection = escape.json_encode([
            {
                'id': 1,
                'name': 'Foo',
                'email': 'foo@example.com',
                'url': 'http://example.com/Foo'
            },
            {
                'id': 2,
                'name': 'Jack',
                'email': 'jack@example.com',
                'url': 'http://example.com/Jack'
            }
        ])

        self.client.next_response = OK, self.json_collection

        self.collection.all(self.stop)
        users, error = self.wait()

        assert_that(not users)

        assert_that(error, instance_of(booby.errors.FieldError))

    def test_when_response_resources_have_extra_fields_and_model_has_decode_method_then_runs_callback_with_error(self):
        self.collection = UsersWithModelDecode(self.client)

        self.json_collection = escape.json_encode([
            {
                'id': 1,
                'name': 'Foo',
                'email': 'foo@example.com',
                'url': 'http://example.com/Foo'
            },
            {
                'id': 2,
                'name': 'Jack',
                'email': 'jack@example.com',
                'url': 'http://example.com/Jack'
            }
        ])

        self.client.next_response = OK, self.json_collection

        self.collection.all(self.stop)
        users, error = self.wait()

        assert_that(not users)

        assert_that(error, instance_of(booby.errors.FieldError))

    def test_when_response_resources_have_extra_fields_but_collection_has_decode_method_then_runs_callback_with_collection(self):
        self.collection = UsersWithCollectionDecode(self.client)

        self.json_collection = escape.json_encode({
            'users': [
                {
                    'id': 1,
                    'name': 'Foo',
                    'email': 'foo@example.com',
                    'url': 'http://example.com/Foo'
                },
                {
                    'id': 2,
                    'name': 'Jack',
                    'email': 'jack@example.com',
                    'url': 'http://example.com/Jack'
                }
            ]
        })

        self.client.next_response = OK, self.json_collection

        self.collection.all(self.stop)
        users, error = self.wait()

        assert_that(not error)
        assert_that(users, contains(
            has_properties(id=1, name=u'Foo', email=u'foo@example.com'),
            has_properties(id=2, name=u'Jack', email=u'jack@example.com')
        ))

    def test_when_response_is_not_found_then_runs_callback_with_http_error(self):
        self.client.next_response = NOT_FOUND, 'Not Found'

        self.collection.all(self.stop)
        users, error = self.wait()

        assert_that(not users)
        assert_that(error, instance_of(errors.HTTPError))
        assert_that(error, has_property('code', NOT_FOUND))

    def test_when_fetching_collection_then_client_performs_http_get_to_collection_url(self):
        self.client.next_response = OK, self.json_collection

        self.collection.all(self.stop)
        self.wait()

        last_request = self.client.last_request

        assert_that(last_request.url, is_('/users'))
        assert_that(last_request.method, is_('GET'))

    def setup(self):
        self.client = fake_httpclient.HTTPClient()
        self.collection = Users(self.client)

        self.json_collection = escape.json_encode([
            {
                'id': 1,
                'name': 'Foo',
                'email': 'foo@example.com'
            },
            {
                'id': 2,
                'name': 'Jack',
                'email': 'jack@example.com'
            }
        ])


class TestQueryCollection(AsyncTestCase):
    def test_when_querying_then_client_performs_http_get_with_requested_params(self):
        self.client.next_response = OK, self.json_collection

        self.collection.query(self.stop, {'name': 'Jack'})
        self.wait()

        last_request = self.client.last_request

        assert_that(last_request.params, is_({'name': 'Jack'}))

    def setup(self):
        self.client = fake_httpclient.HTTPClient()
        self.collection = Users(self.client)

        self.json_collection = escape.json_encode([
            {
                'id': 2,
                'name': 'Jack',
                'email': 'jack@example.com'
            }
        ])


class TestGetModelFromCollection(AsyncTestCase):
    def test_when_response_is_a_json_object_then_runs_callback_with_model(self):
        self.client.next_response = OK, self.json_model

        self.collection.get(1, self.stop)
        user, error = self.wait()

        assert_that(not error)
        assert_that(user, has_properties(id=1, name=u'Foo', email=u'foo@example.com'))

    def test_when_response_is_ok_then_runs_callback_with_persisted_model(self):
        self.client.next_response = OK, self.json_model

        self.collection.get(1, self.stop)
        user, error = self.wait()

        assert_that(not error)
        assert_that(user, has_property('_persisted', True))

    def test_when_response_is_a_json_object_with_extra_fields_but_model_has_not_decode_method_then_runs_callback_with_value_error(self):
        self.json_model = escape.json_encode({
            'id': 1,
            'name': 'Foo',
            'email': 'foo@example.com',
            'url': 'http://example.com/Foo'
        })

        self.client.next_response = OK, self.json_model

        self.collection.get(1, self.stop)
        user, error = self.wait()

        assert_that(not user)

        assert_that(error, instance_of(booby.errors.FieldError))

    def test_when_response_is_a_json_object_with_extra_fields_but_model_has_decode_method_then_runs_callback_with_model(self):
        self.collection = UsersWithModelDecode(self.client)

        self.json_model = escape.json_encode({
            'id': 1,
            'name': 'Foo',
            'email': 'foo@example.com',
            'url': 'http://example.com/Foo'
        })

        self.client.next_response = OK, self.json_model

        self.collection.get(1, self.stop)
        user, error = self.wait()

        assert_that(not error)
        assert_that(user, has_properties(id=1, name=u'Foo', email=u'foo@example.com'))

    def test_when_response_is_not_found_then_runs_callback_with_http_error(self):
        self.client.next_response = NOT_FOUND, 'Not Found'

        self.collection.get(1, self.stop)
        user, error = self.wait()

        assert_that(not user)
        assert_that(error, instance_of(errors.HTTPError))
        assert_that(error, has_property('code', NOT_FOUND))

    def test_when_model_has_not_url_then_client_performs_http_get_using_the_collection_url(self):
        self.client.next_response = OK, self.json_model

        self.collection.get(1, self.stop)
        self.wait()

        last_request = self.client.last_request

        assert_that(last_request.url, is_('/users/1'))
        assert_that(last_request.method, is_('GET'))

    def test_when_model_has_url_attribute_then_client_performs_http_request_with_model_url(self):
        self.collection = UsersWithModelUrl(self.client)

        self.client.next_response = OK, self.json_model

        self.collection.get(1, self.stop)
        self.wait()

        assert_that(self.client.last_request.url, is_('/users-resource/1'))

    def test_when_model_url_contains_query_params_then_client_performs_http_request_with_correct_url(self):
        self.collection = UsersWithModelUrlQuery(self.client)

        self.client.next_response = OK, self.json_model

        self.collection.get(1, self.stop)
        self.wait()

        assert_that(self.client.last_request.url, is_('/users-resource/1?type=json'))

    def test_when_model_has_static_url_method_then_client_performs_http_request_with_returned_url(self):
        self.collection = UsersWithModelStaticUrlMethod(self.client)

        self.client.next_response = OK, self.json_model

        self.collection.get(1, self.stop)
        self.wait()

        assert_that(self.client.last_request.url, is_('/users?id=1'))

    def test_when_collection_url_contains_query_params_then_client_performs_http_request_with_correct_url(self):
        self.collection.url += '?type=json'

        self.client.next_response = OK, self.json_model

        self.collection.get(1, self.stop)
        self.wait()

        assert_that(self.client.last_request.url, is_('/users/1?type=json'))

    def setup(self):
        self.client = fake_httpclient.HTTPClient()
        self.collection = Users(self.client)

        self.json_model = escape.json_encode({
            'id': 1,
            'name': 'Foo',
            'email': 'foo@example.com'
        })


class AddModelMixin(object):
    def test_when_response_is_a_json_object_then_runs_callback_with_model(self):
        self.client.next_response = CREATED, self.json_model

        self.collection.add(self.user, self.stop)
        user, error = self.wait()

        assert_that(not error)
        assert_that(user, is_(self.user))
        assert_that(user, has_properties(id=1, name=u'Foo', email=u'foo@example.com'))

    def test_when_response_is_ok_then_runs_callback_with_persisted_model(self):
        self.client.next_response = CREATED, self.json_model

        self.collection.add(self.user, self.stop)
        user, error = self.wait()

        assert_that(not error)
        assert_that(user, has_property('_persisted', True))

    def test_when_response_is_ok_and_empty_body_then_runs_callback_with_persisted_model(self):
        self.client.next_response = CREATED, ''

        self.collection.add(self.user, self.stop)
        user, error = self.wait()

        assert_that(not error)
        assert_that(user, has_property('_persisted', True))

    def test_when_response_is_a_json_object_with_extra_fields_and_model_has_not_decode_method_then_runs_callback_with_value_error(self):
        self.json_model = escape.json_encode({
            'id': 1,
            'name': 'Foo',
            'email': 'foo@example.com',
            'url': 'http://example.com/Foo'
        })

        self.client.next_response = CREATED, self.json_model

        self.collection.add(self.user, self.stop)
        user, error = self.wait()

        assert_that(not user)

        assert_that(error, instance_of(booby.errors.FieldError))

    def test_when_response_has_location_header_then_use_location_as_model_url(self):
        self.client.next_response = CREATED, '', {'Location': '/users/foo'}

        self.collection.add(self.user, self.stop)
        user, error = self.wait()

        assert_that(not error)
        assert_that(user._url, equal_to('/users/foo'))

    def test_when_response_is_a_json_object_with_extra_fields_but_model_has_decode_method_then_runs_callback_with_model(self):
        self.collection = UsersWithModelDecode(self.client)
        self.user = self.collection.model(**dict(self.user))

        self.json_model = escape.json_encode({
            'id': 1,
            'name': 'Foo',
            'email': 'foo@example.com',
            'url': 'http://example.com/Foo'
        })

        self.client.next_response = CREATED, self.json_model

        self.collection.add(self.user, self.stop)
        user, error = self.wait()

        assert_that(not error)
        assert_that(user, has_properties(id=1, name=u'Foo', email=u'foo@example.com'))

    def test_when_response_is_bad_request_then_runs_callback_with_http_error(self):
        self.client.next_response = BAD_REQUEST, 'Bad Request'

        self.collection.add(self.user, self.stop)
        user, error = self.wait()

        assert_that(not user)
        assert_that(error, instance_of(errors.HTTPError))
        assert_that(error, has_property('code', BAD_REQUEST))

    def test_when_model_has_not_encode_method_then_client_performs_http_request_with_json_body(self):
        self.client.next_response = CREATED, self.json_model

        expected_body = escape.json_encode(dict(self.user))

        self.collection.add(self.user, self.stop)
        self.wait()

        last_request = self.client.last_request

        assert_that(last_request.body, is_(expected_body))
        assert_that(last_request.headers, has_entry('Content-Type', 'application/json'))

    def test_when_model_has_encode_method_then_client_performs_http_request_with_custom_body_and_content_type(self):
        self.client.next_response = CREATED, self.json_model

        self.user = UserWithEncode(name='Foo', email='foo@example.com')

        expected_body = urlencode(dict(self.user))

        self.collection.add(self.user, self.stop)
        self.wait()

        last_request = self.client.last_request

        assert_that(last_request.body, is_(expected_body))
        assert_that(last_request.headers, has_entry('Content-Type', 'application/x-www-form-urlencoded'))


class TestAddNewModelToCollection(AddModelMixin, AsyncTestCase):
    def test_when_creating_model_then_client_performs_http_post_to_collection_url(self):
        self.client.next_response = CREATED, self.json_model

        self.collection.add(self.user, self.stop)
        self.wait()

        last_request = self.client.last_request

        assert_that(last_request.url, is_('/users'))
        assert_that(last_request.method, is_('POST'))

    def setup(self):
        self.client = fake_httpclient.HTTPClient()
        self.collection = Users(self.client)

        self.user = User(name='Foo', email='foo@example.com')

        self.json_model = escape.json_encode({
            'id': 1,
            'name': 'Foo',
            'email': 'foo@example.com'
        })


class TestAddPersistedModelToCollection(AddModelMixin, AsyncTestCase):
    def test_when_model_has_not_url_then_client_performs_http_put_to_collection_url(self):
        self.client.next_response = OK, self.json_model

        self.collection.add(self.user, self.stop)
        self.wait()

        last_request = self.client.last_request

        assert_that(last_request.url, is_('/users/1'))
        assert_that(last_request.method, is_('PUT'))

    def test_when_model_has_url_attribute_then_client_performs_http_request_with_model_url(self):
        self.collection = UsersWithModelUrl(self.client)
        self.user = UserWithUrl(id=1, name='Foo', email='foo@example.com')
        self.user._persisted = True

        self.client.next_response = OK, self.json_model

        self.collection.add(self.user, self.stop)
        self.wait()

        assert_that(self.client.last_request.url, is_('/users-resource/1'))

    def test_when_model_url_contains_query_params_then_client_performs_http_request_with_correct_url(self):
        self.collection = UsersWithModelUrlQuery(self.client)
        self.user = UserWithUrlQuery(id=1, name='Foo', email='foo@example.com')
        self.user._persisted = True

        self.client.next_response = OK, self.json_model

        self.collection.add(self.user, self.stop)
        self.wait()

        assert_that(self.client.last_request.url, is_('/users-resource/1?type=json'))

    def test_when_model_has_static_url_method_then_client_performs_http_request_with_returned_url(self):
        self.collection = UsersWithModelStaticUrlMethod(self.client)
        self.user = self.collection.model(id=1, name='Foo', email='foo@example.com')
        self.user._persisted = True

        self.client.next_response = OK, self.json_model

        self.collection.add(self.user, self.stop)
        self.wait()

        assert_that(self.client.last_request.url, is_('/users?id=1'))

    def setup(self):
        self.client = fake_httpclient.HTTPClient()
        self.collection = Users(self.client)

        self.user = User(id=1, name='Foo', email='foo@example.com')
        self.user._persisted = True

        self.json_model = escape.json_encode({
            'id': 1,
            'name': 'Foo',
            'email': 'foo@example.com'
        })


class TestDelete(AsyncTestCase):
    def test_should_perform_http_delete_to_resource_url(self):
        self.client.next_response = NO_CONTENT, ''

        self.collection.delete(self.user, self.stop)
        self.wait()

        last_request = self.client.last_request

        assert_that(last_request.url, is_('/users/1'))
        assert_that(last_request.method, is_('DELETE'))

    def test_should_run_callback_with_error_if_failed_to_perform_delete(self):
        self.client.next_response = INTERNAL_SERVER_ERROR, 'Internal Server Error'

        self.collection.delete(self.user, self.stop)
        error = self.wait()[0]

        assert_that(error, instance_of(errors.HTTPError))

    def test_should_run_callback_with_none_if_sucessfuly_deleted(self):
        self.client.next_response = NO_CONTENT, ''

        self.collection.delete(self.user, self.stop)
        error = self.wait()[0]

        assert_that(error, is_(None))

    def setup(self):
        self.client = fake_httpclient.HTTPClient()
        self.collection = Users(self.client)

        self.user = User(id=1, name='Foo', email='foo@example.com')
        self.user._persisted = True


class User(Model):
    id = fields.Integer(primary=True)
    name = fields.String()
    email = fields.String()


class UserWithDecode(User):
    def decode(self, response):
        raw = escape.json_decode(response.body)

        return {
            'id': raw['id'],
            'name': raw['name'],
            'email': raw['email']
        }


class UserWithUrl(User):
    _url = '/users-resource'


class UserWithUrlQuery(User):
    _url = '/users-resource?type=json'


class UserWithStaticUrlMethod(User):
    @staticmethod
    def _url(id_):
        return '/users?' + urlencode({'id': id_})


class UserWithEncode(User):
    def encode(self):
        return urlencode(dict(self)), 'application/x-www-form-urlencoded'


class UserWithoutPrimary(User):
    id = fields.Integer()


class Users(Collection):
    model = User
    url = '/users'


class UsersWithCollectionDecode(Users):
    def decode(self, response):
        raw = escape.json_decode(response.body)

        result = []
        for user in raw['users']:
            result.append({
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            })

        return result


class UsersWithModelDecode(Users):
    model = UserWithDecode


class UsersWithModelUrl(Users):
    model = UserWithUrl


class UsersWithModelUrlQuery(Users):
    model = UserWithUrlQuery


class UsersWithModelStaticUrlMethod(Users):
    model = UserWithStaticUrlMethod


class UsersWithoutPrimary(Users):
    model = UserWithoutPrimary
