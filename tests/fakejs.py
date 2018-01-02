# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from mock import Mock

def createElement(tag):
    class MockElement(object):
        def __init__(self):
            self.html_attribs = dict()
        def setAttribute(self, k, v):
            self.html_attribs[k] = v
        def getAttribute(self, k):
            return self.html_attribs[k]
    ret = MockElement()
    return ret

document = Mock(createElement=createElement)

globals = Mock(document=document)

#globals.document = Mock()


def Function(fn):
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
    wrapper.is_fake_js_func = True
    return wrapper

