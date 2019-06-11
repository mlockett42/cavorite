# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import cavorite
import tests.fakejs as js
from cavorite import callbacks
from cavorite import timeouts
import uuid
from cavorite.HTML import *
import pytest


c = cavorite.c
t = cavorite.t
Router = cavorite.Router

# This file contains tests for the setTimeout/ set Interval support
# Note these tests cannot test the full functionality because they
# don't actually run any javascript


class TestTimeoutBehaviour(object):
    def test_script_tags_are_attached_to_body(self, monkeypatch):
        monkeypatch.setattr(cavorite, 'js', js)

        defaulttext = t('Hello world')
        default_p = c('p', [defaulttext])
        defaultroute = c('div', [default_p])

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        scripts = [e for e in js.globals.document.body.children.l if e.tagName.lower() == 'script']

        assert len(scripts) == 8

        defaultroute.attribs = {'class': 'stuff'}
        defaultroute.mount_redraw()

        scripts = [e for e in js.globals.document.body.children.l if e.tagName.lower() == 'script']

        assert len(scripts) == 8

        defaulttext.text = 'Hello world2'
        defaultroute.mount_redraw()

        scripts = [e for e in js.globals.document.body.children.l if e.tagName.lower() == 'script']

        assert len(scripts) == 8

    def test_timeouts_are_routed_correctly(self, monkeypatch):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(timeouts, 'js', js)
        monkeypatch.setattr(timeouts, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        timeouts.initialise_timeout_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        counter = dict()
        counter['count'] = 0
        def dummy_callback():
            counter['count'] += 1

        assert len(timeouts.global_timeout_callbacks) == 0
        assert len(timeouts.global_timeout_val_to_id) == 0
        assert len(timeouts.global_timeout_id_to_val) == 0
        val = timeouts.set_timeout(dummy_callback, 1)
        assert set(timeouts.global_timeout_callbacks.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_timeout_id_to_val.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_timeout_val_to_id.keys()) == {val}

        assert counter['count'] == 0

        js.globals.document.cavorite_timeouthandler(str(dummy_uuid()))

        assert counter['count'] == 1
        assert len(timeouts.global_timeout_callbacks) == 0
        assert len(timeouts.global_timeout_val_to_id) == 0
        assert len(timeouts.global_timeout_id_to_val) == 0

    def test_timeouts_clear_timeout(self, monkeypatch):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(timeouts, 'js', js)
        monkeypatch.setattr(timeouts, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        timeouts.initialise_timeout_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        counter = dict()
        counter['count'] = 0
        def dummy_callback():
            counter['count'] += 1

        assert len(timeouts.global_timeout_callbacks) == 0
        assert len(timeouts.global_timeout_val_to_id) == 0
        assert len(timeouts.global_timeout_id_to_val) == 0
        val = timeouts.set_timeout(dummy_callback, 1)
        assert set(timeouts.global_timeout_callbacks.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_timeout_id_to_val.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_timeout_val_to_id.keys()) == {val}

        assert counter['count'] == 0

        timeouts.clear_timeout(val)

        assert counter['count'] == 0
        assert len(timeouts.global_timeout_callbacks) == 0
        assert len(timeouts.global_timeout_val_to_id) == 0
        assert len(timeouts.global_timeout_id_to_val) == 0

    def test_intervals_are_routed_correctly(self, monkeypatch):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(timeouts, 'js', js)
        monkeypatch.setattr(timeouts, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        timeouts.initialise_timeout_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        counter = dict()
        counter['count'] = 0
        def dummy_callback():
            counter['count'] += 1

        assert len(timeouts.global_interval_callbacks) == 0
        assert len(timeouts.global_interval_val_to_id) == 0
        assert len(timeouts.global_interval_id_to_val) == 0
        val = timeouts.set_interval(dummy_callback, 1)
        assert set(timeouts.global_interval_callbacks.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_interval_id_to_val.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_interval_val_to_id.keys()) == {val}

        assert counter['count'] == 0

        js.globals.document.cavorite_intervalhandler(str(dummy_uuid()))

        assert counter['count'] == 1
        assert set(timeouts.global_interval_callbacks.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_interval_id_to_val.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_interval_val_to_id.keys()) == {val}

    def test_intervals_clear_interval(self, monkeypatch):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(timeouts, 'js', js)
        monkeypatch.setattr(timeouts, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        timeouts.initialise_timeout_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        counter = dict()
        counter['count'] = 0
        def dummy_callback():
            counter['count'] += 1

        assert len(timeouts.global_interval_callbacks) == 0
        assert len(timeouts.global_interval_val_to_id) == 0
        assert len(timeouts.global_interval_id_to_val) == 0
        val = timeouts.set_interval(dummy_callback, 1)
        assert set(timeouts.global_interval_callbacks.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_interval_id_to_val.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_interval_val_to_id.keys()) == {val}

        assert counter['count'] == 0

        js.globals.document.cavorite_intervalhandler(str(dummy_uuid()))

        assert counter['count'] == 1

        assert set(timeouts.global_interval_callbacks.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_interval_id_to_val.keys()) == {str(dummy_uuid())}
        assert set(timeouts.global_interval_val_to_id.keys()) == {val}
        timeouts.clear_interval(val)

        assert counter['count'] == 1
        assert len(timeouts.global_interval_callbacks) == 0
        assert len(timeouts.global_interval_val_to_id) == 0
        assert len(timeouts.global_interval_id_to_val) == 0

class TestTimeoutErrorBehaviour(object):
    def test_timeout_errors_are_handled_correctly(self, monkeypatch, capsys):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(timeouts, 'js', js)
        monkeypatch.setattr(timeouts, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        timeouts.initialise_timeout_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        def dummy_callback():
            assert False

        val = timeouts.set_timeout(dummy_callback, 1)

        with pytest.raises(AssertionError):
            js.globals.document.cavorite_timeouthandler(str(dummy_uuid()))

        out, err = capsys.readouterr()
        assert 'AssertionError' in out

    def test_interval_errors_are_handled_correctly(self, monkeypatch, capsys):
        def dummy_uuid():
            return uuid.UUID('531cb169-91f4-4102-9a0a-2cd5e9659071')

        monkeypatch.setattr(cavorite, 'js', js)
        monkeypatch.setattr(callbacks, 'js', js)
        monkeypatch.setattr(timeouts, 'js', js)
        monkeypatch.setattr(timeouts, 'get_uuid', dummy_uuid)
        callbacks.initialise_global_callbacks()
        timeouts.initialise_timeout_callbacks()

        defaultroute = c('p', 'Hello world')

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        def dummy_callback():
            assert False

        val = timeouts.set_interval(dummy_callback, 1)

        with pytest.raises(AssertionError):
            js.globals.document.cavorite_intervalhandler(str(dummy_uuid()))

        out, err = capsys.readouterr()
        assert 'AssertionError' in out
