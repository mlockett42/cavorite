# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import cavorite.cavorite
import tests.fakejs as js


c = cavorite.cavorite.c
t = cavorite.cavorite.t


class TestTextNode(object):
    def test_text_as_string(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        text_node = t('Hello world')
        assert text_node._render(None) == 'Hello world'


    def test_text_as_callable(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        text_node = t(lambda: 'Hello world')
        assert text_node._render(None) == 'Hello world'


