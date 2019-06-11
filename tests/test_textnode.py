# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import cavorite
import tests.fakejs as js


c = cavorite.c
t = cavorite.t


class TestTextNode(object):
    def test_text_as_string(self, monkeypatch):
        monkeypatch.setattr(cavorite, 'js', js)
        text_node = t('Hello world')
        assert str(text_node._render(None)) == 'Hello world'

    def test_text_as_callable(self, monkeypatch):
        monkeypatch.setattr(cavorite, 'js', js)
        text_node = t(lambda: 'Hello world')
        assert str(text_node._render(None)) == 'Hello world'

        text_node2 = text_node._build_virtual_dom()
        assert text_node2.text == 'Hello world'

class TestTextNodeCloning(object):
    def test_default_original_none(self):
        node = t("hello")
        assert node.original == None

    def test_original_points_correctly_in_virtual_dom(self):
        node = t("hello")
        virtual_node = node._build_virtual_dom()
        assert virtual_node.original == node
        

