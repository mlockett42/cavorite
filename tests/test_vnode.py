# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from ..cavorite import c, t
import sys
import tests.fakejs as js



class TestAttribs(object):
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

