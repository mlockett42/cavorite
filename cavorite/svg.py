# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from . import c
try:
    import js
except ImportError:
    js = None
import copy


class SVGNode(c):
    # SVG nodes need to refer to the relavant namespace
    def _createDOMElement(self, tag):
        return js.globals.document.createElementNS('http://www.w3.org/2000/svg', tag)

    def _build_virtual_dom(self):
        # Build a copy of the Virtual DOM but render each tag as it's based HTML tag
        clone = SVGNode(self.get_tag_name(), copy.copy(self.get_attribs()))
        clone.original = self
        for child in self.get_children():
            clone.children.append(child._build_virtual_dom())
        return clone


svg = SVGNode
