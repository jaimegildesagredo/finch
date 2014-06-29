Finch: RESTful API consumer
===========================

.. image:: http://img.shields.io/pypi/v/finch.svg
    :target: https://pypi.python.org/pypi/finch
    :alt: Latest version

.. image:: http://img.shields.io/pypi/dm/finch.svg
    :target: https://pypi.python.org/pypi/finch
    :alt: Number of PyPI downloads

.. image:: https://secure.travis-ci.org/jaimegildesagredo/finch.svg?branch=master
    :target: http://travis-ci.org/jaimegildesagredo/finch

Finch is an asynchronous `RESTful API` consumer for Python. Finch is focused on remove all of the boilerplate related to consuming http based APIs and provide a high level abstraction to develop API clients. Finch is released under the `Apache 2 license <http://www.apache.org/licenses/LICENSE-2.0.html>`_, so you can `fork <https://github.com/jaimegildesagredo/finch>`_, `contribute <https://github.com/jaimegildesagredo/finch/pulls>`_ and also `report errors and suggestions <https://github.com/jaimegildesagredo/finch/issues>`_ to improve it.

Usage
=====

To start consuming a REST API you first should define the resources you are going to consume. For resources modeling we use the `booby <https://github.com/jaimegildesagredo/booby>`_ data modeling library. So, for example, to get your repos from `github.com` you should define the `Repo` model and the `Repos` collection.

.. code-block:: python

    from booby import Model, fields
    from finch import Collection

    class Repo(Model):
        id = fields.Integer()
        name = fields.String()
        owner = fields.String()
        is_private = fields.Boolean()

        def decode(self, response):
            return parse_repo(json.loads(response.body))

        def __repr__(self):
            return 'Repo({}/{})'.format(self.owner, self.name)

    class Repos(Collection):
        model = Repo

        def __init__(self, username, *args, **kwargs):
            self.username = username

            super(Repos, self).__init__(*args, **kwargs)

        @property
        def url(self):
            return 'https://api.github.com/users/{}/repos'.format(self.username)

        def decode(self, response):
            return [parse_repo(r) for r in json.loads(response.body)]


    def parse_repo(raw):
        return {
            'id': raw['id'],
            'name': raw['name'],
            'owner': raw['owner']['login'],
            'is_private': raw['private']
        }

Now you can fetch your public repos (and also your private repos if you're authenticated).

.. code-block:: python

    from tornado import httpclient, ioloop

    def on_repos(repos, error):
        ioloop.IOLoop.instance().stop()

        if error:
            raise error

        for repo in repos:
            print repo

    repos = Repos('jaimegildesagredo', httpclient.AsyncHTTPClient())
    repos.all(on_repos)

    ioloop.IOLoop.instance().start()

Installation
============

You can install the last stable release of Finch from PyPI using pip or easy_install.

.. code-block:: bash

    $ pip install finch

Also you can install the latest sources from Github.

.. code-block:: bash

    $ pip install -e git+git://github.com/jaimegildesagredo/finch.git#egg=finch

Tests
=====

To run the Finch tests suite you should install the test requirements and run nosetests.

.. code-block:: bash

    $ pip install -r test-requirements.txt
    $ nosetests tests/unit

Status
======

Finch is under active development and there is not a complete documentation yet. By the moment you can read the examples in this repository and read the tests, that are the most up to date documentation. Also I'm working on create a complete API client using Finch and create a good documentation.
