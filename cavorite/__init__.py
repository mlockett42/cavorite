# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
try:
    import js
except ImportError:
    js = None
import copy
import itertools
import re
import uuid
from . import callbacks


class TextNode(object):
    def __init__(self, text):
        self.text = text

    def _render(self, element):
        return js.globals.document.createTextNode(self.text)

    def _build_virtual_dom(self):
        return TextNode(self.text)

    def _get_dom_changes(self, virtual_dom2):
        if self.text != virtual_dom2.text:
            return [(self, virtual_dom2)]
        else:
            return []

t = TextNode


class VNode(object):
    def __init__(self, tag, attribs=None, children=None, cssClass=None, **kwargs):
        self.tag = tag
        self.attribs = dict()
        self.children = []
        self.parent = None
        self.virtual_dom = None
        if children is not None:
            assert isinstance(attribs, dict) or attribs is None, 'attribs must be a dict attribs={} type={}'.format(attribs, type(attribs))
        if attribs is not None and children is not None:
            self.attribs = attribs
            if isinstance(children, list) or callable(children):
                self.children = children
            if isinstance(children, basestring):
                self.children = [TextNode(children)]
        if attribs is None and children is not None:
            self.attribs = { }
            if isinstance(children, list) or callable(children):
                self.children = children
            if isinstance(children, basestring):
                self.children = [TextNode(children)]
        if attribs is not None and children is None:
            # If the first argument after the tag is a list or string it is actually the children
            if isinstance(attribs, dict):
                self.attribs = attribs
            if isinstance(attribs, list):
                self.children = attribs
            if isinstance(attribs, basestring):
                self.children = [TextNode(attribs)]
        if cssClass is not None:
            assert 'class' not in self.attribs, 'Cannot define css class twice'
            self.attribs['class'] = cssClass
        if 'class' in self.attribs and isinstance(self.attribs['class'], list):
            self.attribs['class'] = ' '.join(self.attribs['class'])

        # Make sure no parameters are in both the attribs and the kwargs
        attrib_set = set(self.attribs.keys())
        kwargs_set = set(kwargs.keys())
        assert attrib_set.isdisjoint(kwargs_set)

        # Merge any kwargs into the attribs
        self.attribs.update(kwargs)

        # If we were given the style as a dict make it into a string
        if 'style' in self.attribs and isinstance(self.attribs['style'], dict):
            d = self.attribs['style']
            l = [k + ': ' + v + ';' for k, v in d.items()]
            self.attribs['style'] = ' '.join(l)
        if '_cavorite_id' not in self.attribs:
            self.attribs['_cavorite_id'] = uuid.uuid4().hex


    def render(self, element):
        while element.hasChildNodes():
            element.removeChild(element.lastChild)
        new_element = self._render(element)
        element.appendChild(new_element)

    def get_attribs(self):
        return self.attribs

    def get_children(self):
        if callable(self.children):
            return self.children()
        ret = []
        for child in self.children:
            node = child() if callable(child) else child
            node.parent = self
            ret.append(node)
        return ret
        

    def _render(self, element):
        new_element = js.globals.document.createElement(self.tag)
        self.dom_element = new_element
        for k, v in self.get_attribs().items():
            if k == 'onclick':
                callbacks.global_callbacks['onclick'][self.attribs['_cavorite_id']] = v
                setattr(new_element,k, callbacks.global_onclick_handler)
            elif callable(v):
                new_element.setAttribute(k, v())
            else:
                new_element.setAttribute(k, v)
        for child in self.get_children():
            child_element = child._render(new_element)
            new_element.appendChild(child_element)
        return new_element

    def _build_virtual_dom(self):
        clone = VNode(self.tag, copy.copy(self.attribs))
        for child in self.get_children():
            clone.children.append(child._build_virtual_dom())
        return clone        

    def mount(self, element):
        assert self.parent is None, 'You can only mount the root node'
        self._virtual_dom = self._build_virtual_dom()
        self._virtual_dom.render(element)
        self.mounted_element = element

    def _get_dom_changes(self, virtual_dom2):
        if self.tag != virtual_dom2.tag or self.attribs != virtual_dom2.attribs or \
            len(self.children) != len(virtual_dom2.children):
                return [(self, virtual_dom2)]
        r = [self.children[i]._get_dom_changes(virtual_dom2.children[i]) for i in range(len(self.children))]
        return itertools.chain.from_iterable(r)


    def mount_redraw(self):
        virtual_dom2 = self._build_virtual_dom()
        elements_to_change = self._virtual_dom._get_dom_changes(virtual_dom2)
        if any([live_vnode.parent is None for (live_vnode, new_vnode) in elements_to_change]):
            # If the root node has changed just redraw everything the rest of our logic in irrelevant
            self.render(self.mounted_element)
        else:
            for (live_vnode, new_vnode) in elements_to_change:
                live_parent = live_vnode.parent
                new_element = new_vnode._render()
                i = live_parent.children.index(live_vnode)
                live_parent.children[i] = new_vnode
                live_nvode.dom_element.replaceWith(new_vnode.dom_element)

    def get_root(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_root()
        

c = VNode

class Router(object):
    def __init__(self, routes, defaultroute, dom_element):
        self.routes = routes
        self.defaultroute = defaultroute
        self.dom_element = dom_element
        js.globals.document.body.onhashchange=js.Function(self.onhashchange)

    def route(self):
        url_sections = str(js.globals.window.location.href).split('#!', 1)
        if len(url_sections) == 2:
            url = url_sections[1]
        else:
            url = ''
        route = None
        for k, v in self.routes.items():
            p = re.compile(k)
            m = p.search(url)
            if m:
                route = v
                route.url_kwargs = m.groupdict()
        if route is None:
            route = self.defaultroute
            route.url_kwargs = { }
        route.mount(self.dom_element)
        js.globals.document.body.onhashchange=js.Function(self.onhashchange)

    def onhashchange(self, e):
        self.route()
            

