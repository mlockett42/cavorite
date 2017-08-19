# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import js

class TextNode(object):
    def __init__(self, text):
        self.text = text

    def _output(self):
        return self.text

    def _render(self, element):
        return js.globals.document.createTextNode(self.text)

t = TextNode

class VNode(object):
    def __init__(self, tag, *args):
        self.tag = tag
        assert len(args) <= 2
        self.attribs = dict()
        self.children = list()
        self.parent = None
        if len(args) == 2:
            self.attribs = args[0]
            if isinstance(args[1], list):
                self.children = args[1]
            if isinstance(args[1], basestring):
                self.children = [TextNode(args[1])]
        if len(args) == 1:
            if isinstance(args[0], dict):
                self.attribs = args[0]
            if isinstance(args[0], list):
                self.children = args[0]
            if isinstance(args[0], basestring):
                self.children = [TextNode(args[0])]
        for child in self.children:
            child.parent = self

    def _output(self):
        return "<" + self.tag + "".join([" " + k + '="' + v + '"' for (k, v) in self.attribs.items()]) + \
            ">" + "".join([child._output() for child in self.children]) + "</" + self.tag + ">"

    def render(self, element):
        while element.hasChildNodes():
            element.removeChild(element.lastChild)
        new_element = self._render(element)
        element.appendChild(new_element)

    def _render(self, element):
        new_element = js.globals.document.createElement(self.tag)
        for k, v in self.attribs.items():
            new_element.setAttribute(k, v)
        for child in self.children:
            child_element = child._render(new_element)
            new_element.appendChild(child_element)
        return new_element

c = VNode


