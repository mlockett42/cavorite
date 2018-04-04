# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from .svg import svg

# This file dynamically creates VNode subclasses for some of the more commonly used SVG tags

# Dynamically create classes from https://stackoverflow.com/a/15247892
def ClassFactory(name, BaseClass):
    def __init__(self, attribs=None, children=None, **kwargs):
        BaseClass.__init__(self, name, attribs, children, **kwargs)
    newclass = type(str(name), (BaseClass,),{"__init__": __init__})
    return newclass


svgtagnames = {'circle', 'ellipse', 'line', 'text', 'polygon', 'polyline', 'rect',
                } # For now just a subset required by Binary Crate

# Dynamically insert variables into the global namespace
for tagname in svgtagnames:
    globals()[tagname] = ClassFactory(tagname, svg)

# The svg tag wraps SVG graphics
svg_wrapper = ClassFactory('svg', svg)

