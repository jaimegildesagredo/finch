Changes
=======

0.4.0 (Not released yet)
------------------------

Highlights
^^^^^^^^^^

* Supports tornado >= 3.0, including latest 4.0.2
* Implemented the ``delete`` method in collections.
* Extracted the callbacks for ``all``, ``get``, ``add`` and the new ``delete`` actions as public ``Collection`` methods so can be overridden to achieve custom behaviors.
* Extracted public methods for the creation of requests for ``all``, ``get``, ``add`` and the new ``delete`` actions, so request creation can be overridden as well.
* Collections can now overwrite the ``Collection.on_error`` method to customize response error handling. See `GH-10 <https://github.com/jaimegildesagredo/finch/pull/10>`_.
* Added the ``Collection.query`` method that works like the ``all`` method allowing to pass query string parameters. See `GH-12 <https://github.com/jaimegildesagredo/finch/pull/12>`_.
* Now when an object is added to the collection, if the response contains a ``Location`` header, the object url will be the content of that header. See `GH-11 <https://github.com/jaimegildesagredo/finch/pull/11>`_.

Backwards-incompatible
^^^^^^^^^^^^^^^^^^^^^^

* The former ``Model`` and ``Collection`` ``parse`` method was renamed to ``decode`` and now receive the entire ``response`` object instead of the ``body`` and ``headers`` as two arguments.

0.3.3
-----

Highlights
^^^^^^^^^^

* Now works with booby 0.4.0!
