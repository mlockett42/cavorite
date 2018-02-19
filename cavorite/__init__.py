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


def lazy_eval(v):
    if callable(v):
        return v()
    else:
        return v


class TextNode(object):
    def __init__(self, text):
        self.text = text
        self.original = None

    def _render(self, element):
        ret = js.globals.document.createTextNode(lazy_eval(self.text))
        return ret

    def was_mounted(self):
        pass

    def _build_virtual_dom(self):
        ret = TextNode(lazy_eval(self.text))
        ret.original = self
        return ret

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
        self.original = None
        self.inject_script_tags = False
        self.mount_listeners = list()
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
            children = self.children()
        else:
            children = self.children
        ret = []
        for child in children:
            node = child() if callable(child) else child
            node.parent = self
            ret.append(node)
        return ret

    def _createDOMElement(self, tag):
        return js.globals.document.createElement(tag)
        
    def _render(self, element):
        new_element = self._createDOMElement(self.tag)
        self.dom_element = new_element
        for k, v in self.get_attribs().items():
            if k in callbacks.global_callback_handlers:
                callbacks.global_callbacks[k][self.attribs['_cavorite_id']] = v
                setattr(new_element,k, callbacks.global_callback_handlers[k])
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
        clone.original = self
        for child in self.get_children():
            clone.children.append(child._build_virtual_dom())
        return clone  

    def attach_script_nodes(self, element):
        def add_script_element(script_text):
            scriptTextNode = js.globals.document.createTextNode(script_text)
            scriptElement = js.globals.document.createElement('script')
            scriptElement.appendChild(scriptTextNode)
            element.appendChild(scriptElement)
    
        add_script_element(
"""function cavorite_setTimeout(key, delay) { 
    return setTimeout(function() { 
        document.cavorite_timeouthandler(key); 
        },
        delay);
    };
""")
        
        add_script_element(
"""function cavorite_setInterval(key, delay) { 
    return setInterval(function() { 
        document.cavorite_intervalhandler(key); 
        },
        delay);
    };
""")

        add_script_element(
"""function cavorite_ajaxGet(url, key) { 
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function(){
            var parsedresult = null;
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
                if (xmlhttp.status == 200) {
                    parsedresult = JSON.parse(xmlhttp.responseText);
                }
                document.cavorite_AjaxGetCallback(xmlhttp, key, parsedresult);
            }
        }
        xmlhttp.open("GET", url, true);
        xmlhttp.send();
    }""")    
        add_script_element(
"""function cavorite_ajaxPost(url, key, data) { 
        var formdata = new FormData();    
        var value;
        Object.keys(data).forEach(function(key) {
            value = data[key];
            formdata.append(key, value);
        });
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function(){
            var parsedresult = null;
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
                if (xmlhttp.status == 200) {
                    parsedresult = JSON.parse(xmlhttp.responseText);
                }
                document.cavorite_AjaxPostCallback(xmlhttp, key, parsedresult);
            }
        }
        xmlhttp.open("POST", url, true);
        xmlhttp.send(formdata);
    }""")    
        add_script_element(
"""function cavorite_ajaxPut(url, key, data) { 
        var formdata = new FormData();    
        var value;
        Object.keys(data).forEach(function(key) {
            value = data[key];
            formdata.append(key, value);
        });
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function(){
            var parsedresult = null;
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
                if (xmlhttp.status == 200) {
                    parsedresult = JSON.parse(xmlhttp.responseText);
                }
                document.cavorite_AjaxPutCallback(xmlhttp, key, parsedresult);
            }
        }
        xmlhttp.open("PUT", url, true);
        xmlhttp.send(formdata);
    }""")    
        add_script_element(
"""function cavorite_ajaxDelete(url, key) { 
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function(){
            var parsedresult = null;
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {   // XMLHttpRequest.DONE == 4
                if (xmlhttp.status == 200) {
                    parsedresult = JSON.parse(xmlhttp.responseText);
                }
                document.cavorite_AjaxPutCallback(xmlhttp, key, parsedresult);
            }
        }
        xmlhttp.open("DELETE", url, true);
        xmlhttp.send();
    }""")    

        
    def was_mounted(self):
        if isinstance(self.children, list):
            for child in self.get_children():
                child.was_mounted()

    def mount(self, element):
        assert self.parent is None, 'You can only mount the root node'
        self._virtual_dom = self._build_virtual_dom()
        self._virtual_dom.render(element)
        self.attach_script_nodes(element)
        self.mounted_element = element
        self.was_mounted()

    def _get_dom_changes(self, virtual_dom2):
        if self.tag != virtual_dom2.tag or self.attribs != virtual_dom2.attribs or \
            len(self.children) != len(virtual_dom2.children):
                return [(self, virtual_dom2)]
        r = [self.children[i]._get_dom_changes(virtual_dom2.children[i]) for i in range(len(self.children))]
        return itertools.chain.from_iterable(r)


    def mount_redraw(self):
        virtual_dom2 = self._build_virtual_dom()
        elements_to_change = list(self._virtual_dom._get_dom_changes(virtual_dom2))
        if any([live_vnode.parent is None for (live_vnode, new_vnode) in elements_to_change]):
            # If the root node has changed just redraw everything the rest of our logic in irrelevant
            self.render(self.mounted_element)
            self.attach_script_nodes(self.mounted_element)
        else:
            for (live_vnode, new_vnode) in elements_to_change:
                live_parent = live_vnode.parent
                new_element = new_vnode._render(live_parent)
                i = live_parent.children.index(live_vnode)
                live_parent.children[i] = new_vnode
                live_vnode.dom_element.replaceWith(new_vnode.dom_element)
        self.was_mounted()

    def get_root(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_root()
        
    def on_body_click(self, e):
        # Called by the router if the body element is click. Ie a click not handled elsewhere
        # Is passed on the current view
        pass

    def on_body_mousemove(self, e, change_x, change_y):
        # Called by the router whenever the mouse moves, change_x and change_y are the change since
        # the last move
        pass

c = VNode

class Router(object):
    router = None

    def __init__(self, routes, defaultroute, dom_element):
        self.routes = routes
        self.defaultroute = defaultroute
        self.dom_element = dom_element
        js.globals.document.body.onhashchange=js.Function(self.onhashchange)
        js.globals.document.onclick=js.Function(self.on_body_click)
        Router.router = self
        self.selected_route = None

        @js.Function
        def on_body_mousemove(e):
            #pass
            #print('Global on_body_mousemove called e=', e.clientX, ',', e.clientY)
            if Router.router:
                Router.router.on_body_mousemove(e)

        js.globals.document.onmousemove = on_body_mousemove
        self.on_body_mousemove_js_function = on_body_mousemove
        self.global_mouse_x = 0
        self.global_mouse_y = 0

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
        route.inject_script_tags = True
        route.mount(self.dom_element)
        self.selected_route = route
        self.ResetHashChange()

    def ResetHashChange(self):
        js.globals.document.body.onhashchange=js.Function(self.onhashchange)
        js.globals.document.onclick=js.Function(self.on_body_click)
        js.globals.document.onmousemove = self.on_body_mousemove_js_function

    def onhashchange(self, e):
        self.route()

    def on_body_click(self, e):
        self.selected_route.on_body_click(e)

    def on_body_mousemove(self, e):
        #print('Router.on_body_mousemove called')
        self.selected_route.on_body_mousemove(e, e.clientX - self.global_mouse_x, e.clientY - self.global_mouse_y)
        self.global_mouse_x = e.clientX
        self.global_mouse_y = e.clientY
            
def get_current_hash():
    return str(js.globals.window.location.hash)


