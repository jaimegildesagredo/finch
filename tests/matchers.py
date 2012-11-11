# -*- coding: utf-8 -*-

from hamcrest import *


def has_properties(**kwargs):
    return all_of(*[has_property(k, v) for k, v in kwargs.iteritems()])
