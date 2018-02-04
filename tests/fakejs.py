# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from mock import Mock, MagicMock

class MockJSList(object):
    # Simulates a list in javascript
    def __init__(self):
        self.l = list()

    @property
    def length(self):
        return len(self.l)

    def item(self, i):
        return self.l[i]

    def append(self, e):
        self.l.append(e)

    def remove(self, e):
        self.l.remove(e)
    

class MockElement(object):
    def __init__(self):
        self.html_attribs = dict()
        self.children =  MockJSList()
        self.tagName = None
        self.value = None
    def setAttribute(self, k, v):
        self.html_attribs[k] = v
    def getAttribute(self, k):
        return self.html_attribs.get(k, None)
    def appendChild(self, element):
        self.children.append(element)
    def hasChildNodes(self):
        return len(self.children) > 0
    def removeChild(self, element):
        self.children.remove(element)
    @property
    def lastChild(self):
        return self.children[-1]

def createElement(tag):
    element = MockElement()
    element.tagName = tag
    return element

class MockTextNode(object):
    def __init__(self, text):
        self._text = text
        self.children = MockJSList()

    def __str__(self):
        return self._text

    def getAttribute(self, k):
        return None

def createTextNode(s):
    return MockTextNode(s)

return_get_element_by_id = None

def getElementById(id):
    return return_get_element_by_id[id]

body = MockElement()

document = Mock(createElement=createElement, createTextNode=createTextNode, getElementById=getElementById, body=body)

globals = MagicMock(document=document)

def Function(fn):
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
    wrapper.is_fake_js_func = True
    return wrapper


def IterateElements(node, callback):
    callback(node)
    for child in node.children.l:
        IterateElements(child, callback)


