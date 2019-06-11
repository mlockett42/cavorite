# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from cavorite import c, t
from cavorite.HTML import *
import inspect
import pytest


class TestTags(object):
    def test_all_tags(self):
        for tagname in htmltagnames:
            theclass = globals()[tagname]
            assert inspect.isclass(theclass)
            obj = theclass()
            assert obj.get_tag_name() == tagname

            obj2 = theclass({'class': 'stuff'}, [t('Hello'), t('World')])
            assert obj2.get_attribs()['class'] =='stuff'
            assert '_cavorite_id' in obj2.get_attribs()
            assert len(obj2.get_attribs()) == 2
            children = obj2.get_children()
            assert len(children) == 2
            assert children[0].text == 'Hello'
            assert children[1].text == 'World'

    def test_href(self):
        node = a(cssClass='stuff', href='https://www.google.com')
        assert node.get_attribs()['class'] =='stuff'
        assert node.get_attribs()['href'] =='https://www.google.com'
        assert '_cavorite_id' in node.get_attribs()
        assert len(node.get_attribs()) == 3

    def test_attrib_kwarg_and_arg(self):
        with pytest.raises(AssertionError):
            tag = a({'href': 'https://www.google.com'}, cssClass='stuff', href='https://www.google.com')

    def test_html_button(self):
        node = html_button(cssClass='stuff')
        assert node.get_attribs()['class'] =='stuff'
        assert '_cavorite_id' in node.get_attribs()
        assert len(node.get_attribs()) == 2
