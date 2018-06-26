# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import cavorite.cavorite
import tests.fakejs as js
from cavorite.cavorite import callbacks
from cavorite.cavorite import timeouts
import uuid
from cavorite.cavorite.HTML import *
from mock import Mock
from cavorite.cavorite import ajaxget
import pytest

c = cavorite.cavorite.c
t = cavorite.cavorite.t
Router = cavorite.cavorite.Router

# This file contains tests for the ajax get support
# Note these tests cannot test the full functionality because they
# don't actually run any javascript


class TestAjaxGetBehaviour(object):

    def test_get_requests_are_routed_correctly(self, monkeypatch):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(ajaxget, 'js', js)
        monkeypatch.setattr(ajaxget, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        ajaxget.initialise_ajaxget_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        counter = dict()
        counter['count'] = 0
        def dummy_callback(xmlhttp, response):
            counter['count'] += 1
            assert response == {'hello': 'world'}

        assert len(ajaxget.global_ajaxget_callbacks) == 0
        val = ajaxget.ajaxget('/hello_world', dummy_callback)
        assert set(ajaxget.global_ajaxget_callbacks.keys()) == {str(dummy_uuid())}

        assert counter['count'] == 0

        xmlhttp = Mock()
        js.globals.document.cavorite_AjaxGetCallback(xmlhttp, str(dummy_uuid()), {'hello': 'world'})

        assert counter['count'] == 1
        assert len(ajaxget.global_ajaxget_callbacks) == 0

class TestAjaxPostBehaviour(object):

    def test_post_requests_are_routed_correctly(self, monkeypatch):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(ajaxget, 'js', js)
        monkeypatch.setattr(ajaxget, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        ajaxget.initialise_ajaxget_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        counter = dict()
        counter['count'] = 0
        def dummy_callback(xmlhttp, response):
            counter['count'] += 1
            assert response == 'OK'

        assert len(ajaxget.global_ajaxpost_callbacks) == 0
        val = ajaxget.ajaxpost('/hello_world', {'key': 'value'}, dummy_callback)
        assert set(ajaxget.global_ajaxpost_callbacks.keys()) == {str(dummy_uuid())}

        assert counter['count'] == 0

        xmlhttp = Mock()
        js.globals.document.cavorite_AjaxPostCallback(xmlhttp, str(dummy_uuid()), 'OK')

        assert counter['count'] == 1
        assert len(ajaxget.global_ajaxpost_callbacks) == 0


class TestAjaxPutBehaviour(object):

    def test_put_requests_are_routed_correctly(self, monkeypatch):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(ajaxget, 'js', js)
        monkeypatch.setattr(ajaxget, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        ajaxget.initialise_ajaxget_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        counter = dict()
        counter['count'] = 0
        def dummy_callback(xmlhttp, response):
            counter['count'] += 1
            assert response == 'OK'

        assert len(ajaxget.global_ajaxput_callbacks) == 0
        val = ajaxget.ajaxput('/hello_world', {'key': 'value'}, dummy_callback)
        assert set(ajaxget.global_ajaxput_callbacks.keys()) == {str(dummy_uuid())}

        assert counter['count'] == 0

        xmlhttp = Mock()
        js.globals.document.cavorite_AjaxPutCallback(xmlhttp, str(dummy_uuid()), 'OK')

        assert counter['count'] == 1
        assert len(ajaxget.global_ajaxput_callbacks) == 0

class TestAjaxDeleteBehaviour(object):

    def test_delete_requests_are_routed_correctly(self, monkeypatch):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(ajaxget, 'js', js)
        monkeypatch.setattr(ajaxget, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        ajaxget.initialise_ajaxget_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        counter = dict()
        counter['count'] = 0
        def dummy_callback(xmlhttp, response):
            counter['count'] += 1
            assert response == 'OK'

        assert len(ajaxget.global_ajaxdelete_callbacks) == 0
        val = ajaxget.ajaxdelete('/hello_world', dummy_callback)
        assert set(ajaxget.global_ajaxdelete_callbacks.keys()) == {str(dummy_uuid())}

        assert counter['count'] == 0

        xmlhttp = Mock()
        js.globals.document.cavorite_AjaxDeleteCallback(xmlhttp, str(dummy_uuid()), 'OK')

        assert counter['count'] == 1
        assert len(ajaxget.global_ajaxdelete_callbacks) == 0

class TestAjaxErrorHandlingBehaviour(object):

    def dummy_callback(self, xmlhttp, response):
        assert False

    def dummy_uuid(self):
        return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

    def gen_request_errors_are_handled_correctly(self, monkeypatch, capsys,
                                                 ajax_fn, callback_fn):

        monkeypatch.setattr(cavorite.cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(ajaxget, 'js', js)
        monkeypatch.setattr(ajaxget, 'get_uuid', self.dummy_uuid)
        callbacks.initialise_global_callbacks()
        ajaxget.initialise_ajaxget_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        ajax_fn()

        with pytest.raises(AssertionError):
            callback_fn()

        out, err = capsys.readouterr()
        assert 'AssertionError' in out

    def test_get_request_errors_are_handled_correctly(self, monkeypatch, capsys):
        self.gen_request_errors_are_handled_correctly(monkeypatch, capsys,
            lambda: ajaxget.ajaxget('/hello_world', self.dummy_callback),
            lambda: js.globals.document.cavorite_AjaxGetCallback(Mock(), str(self.dummy_uuid()), 'OK'),
            )

    def test_post_request_errors_are_handled_correctly(self, monkeypatch, capsys):
        self.gen_request_errors_are_handled_correctly(monkeypatch, capsys,
            lambda: ajaxget.ajaxpost('/hello_world', {'key': 'value'}, self.dummy_callback),
            lambda: js.globals.document.cavorite_AjaxPostCallback(Mock(), str(self.dummy_uuid()), 'OK'),
            )

    def test_put_request_errors_are_handled_correctly(self, monkeypatch, capsys):
        self.gen_request_errors_are_handled_correctly(monkeypatch, capsys,
            lambda: ajaxget.ajaxput('/hello_world', {'key': 'value'}, self.dummy_callback),
            lambda: js.globals.document.cavorite_AjaxPutCallback(Mock(), str(self.dummy_uuid()), 'OK'),
            )

    def test_delete_request_errors_are_handled_correctly(self, monkeypatch, capsys):
        self.gen_request_errors_are_handled_correctly(monkeypatch, capsys,
            lambda: ajaxget.ajaxdelete('/hello_world', self.dummy_callback),
            lambda: js.globals.document.cavorite_AjaxDeleteCallback(Mock(), str(self.dummy_uuid()), 'OK'),
            )
