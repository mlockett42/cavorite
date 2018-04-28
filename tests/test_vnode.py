# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import cavorite.cavorite
from cavorite.cavorite import callbacks
import sys
import tests.fakejs as js
import pytest
import uuid
from mock import Mock, patch
from collections import defaultdict
from cavorite.cavorite.HTML import *

c = cavorite.cavorite.c
t = cavorite.cavorite.t


class TestChildren(object):
    def test_children(self):
        node = c('div', [t('Hello'), t('World')])
        children = node.get_children()
        assert len(children) == 2
        assert children[0].text == 'Hello'
        assert children[1].text == 'World'

    def test_child_callables(self):
        # Test that our children can be callables and that they only
        # run when get_children is called
        world_was_run = {'was_run': False}
        def world():
            world_was_run['was_run'] = True
            return t('World')

        node = c('div', [t('Hello'), world])
        assert world_was_run['was_run'] == False
        children = node.get_children()
        assert len(children) == 2
        assert children[0].text == 'Hello'
        assert children[1].text == 'World'
        assert world_was_run['was_run'] == True

    def test_child_kwarg_callable(self):
        hello_world_was_run = {'was_run': False}
        def hello_world():
            hello_world_was_run['was_run'] = True
            return [t('Hello'), t('World')]

        node = c('div', children=hello_world)
        assert hello_world_was_run['was_run'] == False
        children = node.get_children()
        assert len(children) == 2
        assert children[0].text == 'Hello'
        assert children[1].text == 'World'
        assert hello_world_was_run['was_run'] == True

    def test_child_kwarg_list(self):
        node = c('div', children=[t('Hello'), t('World')])
        children = node.get_children()
        assert len(children) == 2
        assert children[0].text == 'Hello'
        assert children[1].text == 'World'

    def test_child_kwarg_and_arg(self):
        with pytest.raises(AssertionError):
            node = c('div', [t('Hello'), t('World')], children=[t('Hello'), t('World')])

    def test_attribs(self):
        node = c('div', {'class': 'stuff'})
        assert node.get_attribs()['class'] =='stuff'
        assert '_cavorite_id' in node.get_attribs()
        assert len(node.get_attribs()) == 2
        assert node.get_children() == []

    def test_get_children_from_callable_sets_parent(self):
        def get_children():
            return [c('p', 'Hello'), c('p', 'World')]

        node = c('div', children=get_children)
        children = node.get_children()
        assert len(children) == 2
        assert children[0].parent == node
        assert children[1].parent == node


class TestAttribs(object):
    def test_attribs(self):
        node = c('div', cssClass='stuff')
        assert node.get_attribs()['class'] =='stuff'
        assert '_cavorite_id' in node.get_attribs()
        assert len(node.get_attribs()) == 2
        assert node.get_children() == []

    def test_kwarg_and_attribs_dict(self):
        with pytest.raises(AssertionError):
            node = c('div', {'class': 'stuff'}, cssClass='stuff')

    def test_class_list_of_strings(self):
        node = c('div', cssClass=['good', 'stuff'])
        assert node.get_attribs()['class'] =='good stuff'
        assert '_cavorite_id' in node.get_attribs()
        assert len(node.get_attribs()) == 2

    def test_attribs_can_be_callables(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        def class_callback():
            return value
        node = c('div', {'class': class_callback})

        value = 'hello'
        rendered_node = node._render()
        assert rendered_node.getAttribute('class') == 'hello'
        
        value = 'world'
        rendered_node = node._render()
        assert rendered_node.getAttribute('class') == 'world'

class TestStyle(object):
    def test_text_style(self):
        node = c("div", {'style':"padding: 0px 10px 0px 0px; color:white;"})
        assert node.get_attribs()['style'] == "padding: 0px 10px 0px 0px; color:white;"

    def test_dict_style(self):
        node = c("div", {'style':{"padding": "0px 10px 0px 0px", "color":"white"}})
        assert node.get_attribs()['style'] == "padding: 0px 10px 0px 0px; color: white;" or \
            node.get_attribs()['style'] == "color:w hite; padding: 0px 10px 0px 0px;", node.get_attribs()['style']


def validate_uuid4(uuid_string):

    """
    Validate that a UUID string is in
    fact a valid uuid4.

    Happily, the uuid module does the actual
    checking for us.

    It is vital that the 'version' kwarg be passed
    to the UUID() call, otherwise any 32-character
    hex string is considered valid.

    From: https://gist.github.com/ShawnMilo/7777304
    """

    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        # If it's a value error, then the string 
        # is not a valid hex code for a UUID.
        return False

    # If the uuid_string is a valid hex code, 
    # but an invalid uuid4,
    # the UUID.__init__ will convert it to a 
    # valid uuid4. This is bad for validation purposes.

    return val.hex == uuid_string

class TestNodeIDs(object):
    def test_valid_node_id(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        node = c("div")
        assert validate_uuid4(node.attribs['_cavorite_id'])
        rendered_node = node._render()
        assert rendered_node.getAttribute('_cavorite_id') == node.attribs['_cavorite_id']

class TestCallables(object):
    def test_build_dom_makes_js_func(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        callbacks.initialise_global_callbacks()
        def dummy_callback():
            pass
        node = c("div", {'onclick': dummy_callback,
                         'onchange': dummy_callback,
                         'oncontextmenu': dummy_callback,
                         'ondblclick': dummy_callback,
                         'onmousedown': dummy_callback,
                         'onmouseenter': dummy_callback,
                         'onmouseleave': dummy_callback,
                         'onmousemove': dummy_callback,
                         'onmouseover': dummy_callback,
                         'onmouseup': dummy_callback})
        rendered_node = node._render()
        assert rendered_node.onclick.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.onclick != dummy_callback, 'We need to actually wrap that function'
        assert rendered_node.onchange.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.onchange != dummy_callback, 'We need to actually wrap that function'
        assert rendered_node.oncontextmenu.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.oncontextmenu != dummy_callback, 'We need to actually wrap that function'
        assert rendered_node.ondblclick.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.ondblclick != dummy_callback, 'We need to actually wrap that function'
        assert rendered_node.onmousedown.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.onmousedown != dummy_callback, 'We need to actually wrap that function'
        assert rendered_node.onmouseenter.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.onmouseenter != dummy_callback, 'We need to actually wrap that function'
        assert rendered_node.onmouseleave.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.onmouseleave != dummy_callback, 'We need to actually wrap that function'
        assert rendered_node.onmousemove.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.onmousemove != dummy_callback, 'We need to actually wrap that function'
        assert rendered_node.onmouseover.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.onmouseover != dummy_callback, 'We need to actually wrap that function'
        assert rendered_node.onmouseup.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.onmouseup != dummy_callback, 'We need to actually wrap that function'
        
    def test_click_routing(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        callbacks.initialise_global_callbacks()
        counter = {'counter': 0}
        def dummy_callback(e):
            counter['counter'] += 1
        node = c("div", {'onclick': dummy_callback,
                         'onchange': dummy_callback,
                         'oncontextmenu': dummy_callback,
                         'ondblclick': dummy_callback,
                         'onmousedown': dummy_callback,
                         'onmouseenter': dummy_callback,
                         'onmouseleave': dummy_callback,
                         'onmousemove': dummy_callback,
                         'onmouseover': dummy_callback,
                         'onmouseup': dummy_callback})
        rendered_node = node._render()
        global_callbacks = callbacks.global_callbacks
        assert global_callbacks == {'onclick': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    'onchange': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    'oncontextmenu': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    'ondblclick': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    'onmousedown': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    'onmouseenter': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    'onmouseleave': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    'onmousemove': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    'onmouseover': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    'onmouseup': {rendered_node.getAttribute('_cavorite_id'): dummy_callback},
                                    }

        e = Mock(target=rendered_node)
        rendered_node.onclick(e)
        assert counter['counter'] == 1
        rendered_node.onchange(e)
        assert counter['counter'] == 2
        rendered_node.oncontextmenu(e)
        assert counter['counter'] == 3
        rendered_node.ondblclick(e)
        assert counter['counter'] == 4
        rendered_node.onmousedown(e)
        assert counter['counter'] == 5
        rendered_node.onmouseenter(e)
        assert counter['counter'] == 6
        rendered_node.onmouseleave(e)
        assert counter['counter'] == 7
        rendered_node.onmousemove(e)
        assert counter['counter'] == 8
        rendered_node.onmouseover(e)
        assert counter['counter'] == 9
        rendered_node.onmouseup(e)
        assert counter['counter'] == 10

class TestVNodeCloning(object):
    def test_default_original_none(self):
        node = c("div")
        assert node.original == None

    def test_original_points_correctly_in_virtual_dom(self):
        node = c("div")
        virtual_node = node._build_virtual_dom()
        assert virtual_node.original == node

class TestMockElementIteration(object):
    def test_mockelement_iteration(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)

        d = defaultdict(int)

        def mock_element_iterator_callback(node):
            d['calls'] += 1
            if isinstance(node, js.MockElement) and node.tagName == 'div':
                d['div'] += 1
            if isinstance(node, js.MockElement) and node.tagName == 'a' and node.getAttribute('href') == 'https://google.com/':
                d['a_google'] += 1
            if isinstance(node, js.MockElement) and node.tagName == 'p' and len(node.children.l) == 1:
                child = node.children.item(0)
                if isinstance(child, js.MockTextNode) and str(child) == 'Google':
                    d['p_google'] += 1
            if isinstance(node, js.MockTextNode) and str(node) == 'Google':
                d['t_google'] += 1
        
        node = c("div", [
                 c("a", {'href': 'https://google.com/'}, [
                   c("p", "Google"),
                 ]),
               ])
        rendered_node = node._render()
        js.IterateElements(rendered_node, mock_element_iterator_callback)

        # Test we are called once per node
        assert d['calls'] == 4
        assert d['div'] == 1
        assert d['a_google'] == 1
        assert d['p_google'] == 1
        assert d['t_google'] == 1


class TestDiffingElements(object):
    def test_cavorite_id_changes_dont_cause_redraws(self):
        # Don't report that the DOM changed if the cavorite ID is the only thing that changed
        
        class GoogleLink(a):
            def __init__(self):
                super(GoogleLink, self).__init__({'href': 'https://google.com/'}, None)

            def get_children(self):
                return [
                   c("p", "Google"),
                 ]

        node = c("div", [
                 GoogleLink(),
               ])

        node._virtual_dom = node._build_virtual_dom()

        # Because we create a new p element in the GoogleLink's get_children function It's _cavorite_id will change
        virtual_dom2 = node._build_virtual_dom()
        
        assert len(list(node._virtual_dom._get_dom_changes(virtual_dom2))) == 0

    def test_other_node_changes_do_cause_redraws(self):
        # Don't report that the DOM changed if the cavorite ID is the only thing that changed

        theclass = 'Red'
        
        class GoogleLink(a):
            def __init__(self):
                super(GoogleLink, self).__init__({'href': 'https://google.com/'}, None)

            def get_children(self):
                return [
                   c("p", {'class': theclass}, "Google"),
                 ]

        node = c("div", [
                 GoogleLink(),
               ])

        node._virtual_dom = node._build_virtual_dom()

        theclass = 'Blue'

        # Because we the class comes from out of scope variable theclass the node should redraw
        virtual_dom2 = node._build_virtual_dom()
        
        assert len(list(node._virtual_dom._get_dom_changes(virtual_dom2))) == 1

    def test_other_number_of_children_changes_do_not_cause_redraws(self):
        # Don't report that the DOM changed if the cavorite ID is the only thing that changed

        number = 1
        
        class TheList(ul):
            def __init__(self):
                super(TheList, self).__init__()

            def get_children(self):
                return [ol("Hello")] * number

        node = c("div", [
                 TheList(),
               ])

        node._virtual_dom = node._build_virtual_dom()

        number = 2

        # Because we the class comes from out of scope variable theclass the node should redraw
        virtual_dom2 = node._build_virtual_dom()
        
        changes = list(node._virtual_dom._get_dom_changes(virtual_dom2))
        assert len(changes) == 1
        assert changes[0][0].tag == 'ul'

    def test_was_mounted_only_called_on_vnode_which_have_changed(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        # Don't report that the DOM changed if the cavorite ID is the only thing that changed

        theclass = 'Red'
        
        class GoogleLink(a):
            def __init__(self):
                super(GoogleLink, self).__init__(None, None)
                self.was_mounted = Mock()

            def get_children(self):
                return [
                   c("p", "Google"),
                 ]

            def get_attribs(self):
                attribs = super(GoogleLink, self).get_attribs()
                attribs.update({'href': 'https://google.com/', 'class': theclass})
                return attribs

        node = c("div", [
                 GoogleLink(),
               ])

        node.was_mounted = Mock()

        #node._virtual_dom = node._build_virtual_dom()
        body = js.globals.document.body
        node.mount(body)

        div1 = node._virtual_dom
        assert div1.__class__ == c
        assert div1.tag == 'div'
        assert len(div1.children) == 1
        a1 = div1.children[0]
        assert a1.tag == 'a'
        assert a1.__class__ == c
        assert a1.attribs['class'] == 'Red'


        theclass = 'Blue'

        # Because we the class comes from out of scope variable theclass the node should redraw
        virtual_dom2 = node._build_virtual_dom()

        assert len(list(node._virtual_dom._get_dom_changes(virtual_dom2))) == 1

        node.mount_redraw()

        div1 = node._virtual_dom
        assert div1.__class__ == c
        assert div1.tag == 'div'
        assert len(div1.children) == 1
        a1 = div1.children[0]
        assert a1.tag == 'a'
        assert a1.__class__ == c
        assert a1.attribs['class'] == 'Blue'

    def test_attrib_values_can_be_callables_which_are_lazily_evaluated(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        # Don't report that the DOM changed if the cavorite ID is the only thing that changed

        theclass = 'Red'
        
        class GoogleLink(a):
            def __init__(self):
                super(GoogleLink, self).__init__(None, None)
                self.was_mounted = Mock()

            def get_children(self):
                return [
                   c("p", "Google"),
                 ]

            def link_onclick(self, e):
                pass

            def get_attribs(self):
                attribs = super(GoogleLink, self).get_attribs()
                attribs.update({'href': 'https://google.com/', 'class': lambda : theclass, 'onclick': self.link_onclick})
                return attribs

        node = c("div", [
                 GoogleLink(),
               ])

        node.was_mounted = Mock()

        google_link = node.children[0]
        assert google_link.__class__ == GoogleLink
        assert google_link.get_lazy_eval_attribs()['class'] == 'Red'
        assert callable(google_link.get_lazy_eval_attribs()['onclick'])

        #node._virtual_dom = node._build_virtual_dom()
        body = js.globals.document.body
        node.mount(body)

        div1 = node._virtual_dom
        assert div1.__class__ == c
        assert div1.tag == 'div'
        assert len(div1.children) == 1
        a1 = div1.children[0]
        assert a1.tag == 'a'
        assert a1.__class__ == c
        assert a1.attribs['class'] == 'Red'
        assert callable(a1.attribs['onclick'])


        theclass = 'Blue'

        # Because we the class comes from out of scope variable theclass the node should redraw
        virtual_dom2 = node._build_virtual_dom()

        assert len(list(node._virtual_dom._get_dom_changes(virtual_dom2))) == 1

        node.mount_redraw()

        div1 = node._virtual_dom
        assert div1.__class__ == c
        assert div1.tag == 'div'
        assert len(div1.children) == 1
        a1 = div1.children[0]
        assert a1.tag == 'a'
        assert a1.__class__ == c
        assert a1.attribs['class'] == 'Blue'
        assert callable(a1.attribs['onclick'])


