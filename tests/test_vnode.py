# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import cavorite.cavorite
from cavorite.cavorite import callbacks
import sys
import tests.fakejs as js
import pytest
import uuid
from mock import Mock


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
        rendered_node = node._render(None)
        assert rendered_node.getAttribute('class') == 'hello'
        
        value = 'world'
        rendered_node = node._render(None)
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
        rendered_node = node._render(None)
        assert rendered_node.getAttribute('_cavorite_id') == node.attribs['_cavorite_id']

class TestCallables(object):
    def test_build_dom_makes_js_func(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        callbacks.initialise_global_callbacks()
        def dummy_callback():
            pass
        node = c("div", {'onclick': dummy_callback})
        rendered_node = node._render(None)
        assert rendered_node.onclick.is_fake_js_func, 'Check is a function wrapped by js.Function'
        assert rendered_node.onclick != dummy_callback, 'We need to actually wrap that function'
        
    def test_click_routing(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        callbacks.initialise_global_callbacks()
        counter = {'counter': 0}
        def dummy_callback(e):
            counter['counter'] += 1
        node = c("div", {'onclick': dummy_callback})
        rendered_node = node._render(None)
        global_callbacks = callbacks.global_callbacks
        assert global_callbacks == {'onclick': {rendered_node.getAttribute('_cavorite_id'): dummy_callback}}

        e = Mock(target=rendered_node)
        rendered_node.onclick(e)
        assert counter['counter'] == 1

        
