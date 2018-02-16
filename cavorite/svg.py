# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from . import c
try:
    import js
except ImportError:
    js = None


class SVGNode(c):
    def _createDOMElement(self, tag):
        return js.globals.document.createElementNS('http://www.w3.org/2000/svg', tag)


svg = SVGNode

