# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from mock import Mock

class MockElement(object):
    def __init__(self):
        self.html_attribs = dict()
        self.children =  list()
        self.tagName = None
    def setAttribute(self, k, v):
        self.html_attribs[k] = v
    def getAttribute(self, k):
        return self.html_attribs[k]
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

def createTextNode(s):
    return s

body = MockElement()

document = Mock(createElement=createElement, createTextNode=createTextNode, body=body)

globals = Mock(document=document)

def Function(fn):
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
    wrapper.is_fake_js_func = True
    return wrapper



