# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import cavorite.cavorite
import cavorite.cavorite.HTML
import inspect
import pytest
from mock import Mock
import cavorite.cavorite.bootstrap.modals
import tests.fakejs as js

div = cavorite.cavorite.HTML.div
label = cavorite.cavorite.HTML.label
html_input = cavorite.cavorite.HTML.html_input
select = cavorite.cavorite.HTML.select
option = cavorite.cavorite.HTML.option

Modal = cavorite.cavorite.bootstrap.modals.Modal

class TestModals(object):
    def test_we_correctly_retreive_form_data(self, monkeypatch):
        #rendered_modal = 1
        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(cavorite.cavorite.bootstrap.modals, 'js', js)
        #monkeypatch.setattr(cavorite.cavorite.bootstrap.modals.js, 'getElementById', Mock(return_value=rendered_modal))
        onclick = Mock()

        m =   Modal("createNew", "Create New", [
                div({'class': 'form-group'}, [
                  label({'class': 'col-form-label', 'for': 'txtProjectName'}, 'Title'),
                  html_input({'type': 'text', 'class': 'form-control', 'id': 'txtProjectName', 'placeholder': "Title of project"}),
                ]),
                #div({'class': 'form-group'}, [
                #  label({'for': 'exampleFormControlTextarea1'}, 'Description'),
                #  textarea({'class': 'form-control', 'id':"exampleFormControlTextarea1", 'placeholder':"Description of project", 'rows':"3"}),
                #]),
                div({'class': 'form-group'}, [
                  label({'for': 'selectProjectType'}, 'Project Type'),
                  select({'class': 'form-control', 'id': 'selectProjectType'}, [
                    option({'value': 0}, 'Python'),
                  ]),
                ]),
              ], onclick)

        #print('TestModals getElementById=', js.getElementById('a'))

        rendered_modal = m._render(None)
        cavorite.cavorite.bootstrap.modals.js.return_get_element_by_id = {'createNew': rendered_modal}

        result = dict()

        def setup_mock_modal_callback(node):
            if isinstance(node, js.MockElement) and node.getAttribute('id') == 'txtProjectName':
                node.value = 'Hello world'
            if isinstance(node, js.MockElement) and node.getAttribute('id') == 'selectProjectType':
                node.value = 0
            if isinstance(node, js.MockElement) and node.getAttribute('class') == 'btn btn-primary':
                result['ok_button'] = node

        js.IterateElements(rendered_modal, setup_mock_modal_callback)

        # Simulate the OK click
        e = Mock(target=result['ok_button'])
        m.handle_ok(e)

        onclick.assert_called_with(e, {'txtProjectName': 'Hello world', 'selectProjectType': 0})

