# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from ..cavorite import c, t
from ..cavorite.HTML import *
import inspect
import pytest


class TestTags(object):
    def test_all_tags(self):
        for tagname in htmltagnames:
            theclass = globals()[tagname]
            assert inspect.isclass(theclass)
            obj = theclass()
            assert obj.tag == tagname

            obj2 = theclass({'class': 'stuff'}, [t('Hello'), t('World')])
            assert obj2.get_attribs() == {'class': 'stuff'}
            children = obj2.get_children()
            assert len(children) == 2
            assert children[0].text == 'Hello'
            assert children[1].text == 'World'

    def test_href(self):
        tag = a(cssClass='stuff', href='https://www.google.com')
        assert tag.get_attribs() == {'class': 'stuff',  'href':'https://www.google.com'}

    def test_attrib_kwarg_and_arg(self):
        with pytest.raises(AssertionError):
            tag = a({'href': 'https://www.google.com'}, cssClass='stuff', href='https://www.google.com')

    def test_html_button(self):
        tag = html_button(cssClass='stuff')
        assert tag.get_attribs() == {'class': 'stuff'}

    

