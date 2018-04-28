# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import cavorite.cavorite
import tests.fakejs as js
from collections import defaultdict
import cavorite.cavorite.svg
from ..cavorite.svg_wrapper import *

c = cavorite.cavorite.c
svg = cavorite.cavorite.svg.svg


class TestMockElementIteration(object):
    def test_svg_creation(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(cavorite.cavorite.svg, 'js', js)

        d = defaultdict(int)

        def mock_element_iterator_callback(node):
            d['calls'] += 1
            if isinstance(node, js.MockElement) and node.tagName == 'div':
                d['div'] += 1
            if isinstance(node, js.MockElementSVG) and node.tagName == 'svg' and \
               node.getAttribute('height') == '500' and node.getAttribute('width') == '600':
                d['svg_element'] += 1
            if isinstance(node, js.MockElementSVG) and node.tagName == 'line' and \
               node.getAttribute('x1') == '5' and node.getAttribute('y1') == '5' and \
               node.getAttribute('x2') == '350' and node.getAttribute('y2') == '360' and \
               node.getAttribute('style') == 'stroke:rgb(255,0,0);stroke-width:2':
                d['svg_line'] += 1
        
        node = c("div", [
                 svg("svg", {'height': '500', 'width': '600'}, [
                   svg("line", {'x1': '5', 'y1': '5', 'x2': '350', 'y2': '360', 'style': "stroke:rgb(255,0,0);stroke-width:2"}),
                 ]),
               ])
        rendered_node = node._render()
        js.IterateElements(rendered_node, mock_element_iterator_callback)

        # Test we are called once per node
        assert d['calls'] == 3
        assert d['div'] == 1
        assert d['svg_element'] == 1
        assert d['svg_line'] == 1

    def test_svg_wrapper_classes_creation(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(cavorite.cavorite.svg, 'js', js)

        d = defaultdict(int)

        def mock_element_iterator_callback(node):
            d['calls'] += 1
            if isinstance(node, js.MockElement) and node.tagName == 'div':
                d['div'] += 1
            if isinstance(node, js.MockElementSVG) and node.tagName == 'svg' and \
               node.getAttribute('height') == '500' and node.getAttribute('width') == '600':
                d['svg_element'] += 1
            if isinstance(node, js.MockElementSVG) and node.tagName == 'line' and \
               node.getAttribute('x1') == '5' and node.getAttribute('y1') == '5' and \
               node.getAttribute('x2') == '350' and node.getAttribute('y2') == '360' and \
               node.getAttribute('style') == 'stroke:rgb(255,0,0);stroke-width:2':
                d['svg_line'] += 1
        
        node = c("div", [
                 svg_wrapper({'height': '500', 'width': '600'}, [
                   line({'x1': '5', 'y1': '5', 'x2': '350', 'y2': '360', 'style': "stroke:rgb(255,0,0);stroke-width:2"}),
                 ]),
               ])
        rendered_node = node._render()
        js.IterateElements(rendered_node, mock_element_iterator_callback)

        # Test we are called once per node
        assert d['calls'] == 3
        assert d['div'] == 1
        assert d['svg_element'] == 1
        assert d['svg_line'] == 1


