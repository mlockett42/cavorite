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


