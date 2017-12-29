# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from ..cavorite import c, t
import sys
import tests.fakejs as js
import pytest


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
        assert node.get_attribs() == {'class': 'stuff'}
        assert node.get_children() == []


class TestAttribs(object):
    def test_attribs(self):
        node = c('div', cssClass='stuff')
        assert node.get_attribs() == {'class': 'stuff'}
        assert node.get_children() == []

    def test_kwarg_and_attribs_dict(self):
        with pytest.raises(AssertionError):
            node = c('div', {'class': 'stuff'}, cssClass='stuff')

    def test_class_list_of_strings(self):
        node = c('div', cssClass=['good', 'stuff'])
        assert node.get_attribs() == {'class': 'good stuff'}
        

