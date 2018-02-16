# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from .svg import svg


def ClassFactory(name, BaseClass):
    def __init__(self, attribs=None, children=None, **kwargs):
        BaseClass.__init__(self, name, attribs, children, **kwargs)
    newclass = type(str(name), (BaseClass,),{"__init__": __init__})
    return newclass


svgtagnames = {'circle', 'ellipse', 'line', 'text', 'polygon', 'polyline', 'rect',
                } # For now just a subset required by Binary Crate

for tagname in svgtagnames:
    globals()[tagname] = ClassFactory(tagname, svg)

svg_wrapper = ClassFactory('svg', svg)

