# -*- coding: utf-8 -*-


from tornado import testing


class AsyncTestCase(testing.AsyncTestCase):
    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.setup()

    def setup(self):
        pass

    def stop(self, *args, **kwargs):
        """
        Allows the default stop() method to store multiple
        positional arguments when used as test callback along
        with the wait() method.

        """

        super(AsyncTestCase, self).stop(args, **kwargs)
