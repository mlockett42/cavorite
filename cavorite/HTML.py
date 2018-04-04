# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from . import c

# This file dynamically creates VNode subclasses for each known HTML tag

# Dynamically create classes from https://stackoverflow.com/a/15247892
def ClassFactory(name, BaseClass):
    def __init__(self, attribs=None, children=None, **kwargs):
        BaseClass.__init__(self, name, attribs, children, **kwargs)
    newclass = type(str(name), (BaseClass,),{"__init__": __init__})
    return newclass

htmltagnames = {'a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article',
                'aside', 'audio', 'b', 'base', 'basefont', 'bdi', 'bdo', 'big',
                'blockquote', 'body', 'br', 'canvas', 'caption',
                'center', 'cite', 'code', 'col', 'colgroup', 'datalist', 'dd',
                'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt',
                'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 
                'footer', 'form', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4',
                'h5', 'h6', 'head', 'header', 'hr', 'html', 'i', 'iframe', 
                'img', 'ins', 'kbd', 'label', 'legend', 'li', 'link',
                'main', 'map', 'mark', 'menu', 'menuitem', 'meta', 'meter', 
                'nav', 'noframes', 'noscript', 'ol', 'optgroup', 
                'option', 'output', 'p', 'param', 'picture', 'pre', 'progress',
                'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section',
                'select', 'small', 'source', 'span', 'strike', 'strong',
                'style', 'sub', 'summary', 'sup', 'table', 'tbody', 'td',
                'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr',
                'track', 'tt', 'u', 'ul', 'var', 'video', 'wbr'
                }

# Dynamically insert variables into the global namespace
for tagname in htmltagnames:
    globals()[tagname] = ClassFactory(tagname, c)

# These need to be given different names because they conflict with standard
# python names
html_button = ClassFactory('button', c)
html_input = ClassFactory('input', c)
html_object = ClassFactory('object', c)
html_dir = ClassFactory('dir', c)
