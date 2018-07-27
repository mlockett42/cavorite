# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from cavorite.cavorite import callbacks
from mock import Mock
import tests.fakejs as js
import pytest


class TestCallbackExceptionHandling(object):
    def performTest(self, handler_name, monkeypatch, capsys):
        monkeypatch.setattr(callbacks, 'js', js)

        def fail_now(e):
            assert False

        target = js.createElement('button')
        target.html_attribs['_cavorite_id'] = '41a2b617-3dfe-4f39-8a14-58bea7459db2'

        callbacks.initialise_global_callbacks()
        callbacks.global_callbacks[handler_name][
            '41a2b617-3dfe-4f39-8a14-58bea7459db2'] = fail_now

        with pytest.raises(AssertionError):
            callbacks.global_callback_handlers[handler_name](Mock(target=target))

        out, err = capsys.readouterr()
        assert 'AssertionError' in out

    def test_exceptions_in_onclick_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('onclick', monkeypatch, capsys)

    def test_exceptions_in_onchange_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('onchange', monkeypatch, capsys)

    def test_exceptions_in_oncontextmenu_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('oncontextmenu', monkeypatch, capsys)

    def test_exceptions_in_ondblclick_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('ondblclick', monkeypatch, capsys)

    def test_exceptions_in_onmousedown_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('onmousedown', monkeypatch, capsys)

    def test_exceptions_in_onmouseenter_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('onmouseenter', monkeypatch, capsys)

    def test_exceptions_in_onmouseleave_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('onmouseleave', monkeypatch, capsys)

    def test_exceptions_in_onmousemove_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('onmousemove', monkeypatch, capsys)

    def test_exceptions_in_onmouseup_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('onmouseup', monkeypatch, capsys)

    def test_exceptions_in_onsubmit_callbacks_are_handled(self, monkeypatch, capsys):
        self.performTest('onsubmit', monkeypatch, capsys)
