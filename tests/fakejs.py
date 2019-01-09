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
        self.checked = None
    def setAttribute(self, k, v):
        self.html_attribs[k] = v
    def getAttribute(self, k):
        return self.html_attribs.get(k, None)
    def appendChild(self, element):
        self.children.append(element)
    def hasChildNodes(self):
        return len(self.children.l) > 0
    def removeChild(self, element):
        self.children.remove(element)
    @property
    def lastChild(self):
        return self.children.l[-1]
    @property
    def options(self):
        assert self.tagName.lower() == 'select' # Only select's may have options
        # Options is a JSList of all of our children that are option tags
        ret = MockJSList()
        ret.l = [e for e in self.children.l if e.tagName == 'option']
        return ret

class MockElementSVG(MockElement):
    pass

def createElement(tag):
    element = MockElement()
    element.tagName = tag
    return element

def createElementNS(ns, tag):
    if ns == 'http://www.w3.org/2000/svg':
        element = MockElementSVG()
        element.tagName = tag
        return element
    assert False

class MockTextNode(object):
    def __init__(self, text):
        self._text = text
        self.children = MockJSList()

    def __str__(self):
        return self._text

    def getAttribute(self, k):
        return None

    def replaceWith(self, node):
        pass

def createTextNode(s):
    return MockTextNode(s)

return_get_element_by_id = None

def getElementById(id):
    return return_get_element_by_id[id]

return_get_elements_by_class_name = None

def getElementsByClassName(class_name):
    return return_get_elements_by_class_name[class_name]

body = MockElement()

document = Mock(createElement=createElement,
                createElementNS=createElementNS,
                createTextNode=createTextNode,
                getElementById=getElementById,
                getElementsByClassName=getElementsByClassName,
                body=body)

window = MagicMock(innerHeight=800)

globals = MagicMock(document=document, window=window)

def Function(fn):
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
    wrapper.is_fake_js_func = True
    return wrapper


def IterateElements(node, callback):
    callback(node)
    for child in node.children.l:
        IterateElements(child, callback)

null = None
