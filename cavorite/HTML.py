# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from . import c


# Dynamically create classes from https://stackoverflow.com/a/15247892
def ClassFactory(name, BaseClass):
    def __init__(self, attribs=None, children=None, **kwargs):
        BaseClass.__init__(self, name, attribs, children, **kwargs)
    newclass = type(str(name), (BaseClass,),{"__init__": __init__})
    return newclass

htmltagnames = {'a', 'i', 'li', 'span', 'div', 'center', 'ul', 'nav',
                'button', 'span', 'form', 'footer', 'small', 'p'}

for tagname in htmltagnames:
    globals()[tagname] = ClassFactory(tagname, c)

html_button = button
