# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import cavorite
import tests.fakejs as js
from cavorite import callbacks
from cavorite import timeouts
import uuid
from cavorite.HTML import *

c = cavorite.c
t = cavorite.t
Router = cavorite.Router


class TestMountListener(object):
    def test_mount_listener(self, monkeypatch):
        monkeypatch.setattr(cavorite, 'js', js)

        counter = {'count': 0}
        def dummy_callback():
            counter['count'] += 1

        class My_C(c):
            def was_mounted(self):
                dummy_callback()
                super(My_C, self).was_mounted()

        class My_T(t):
            def was_mounted(self):
                dummy_callback()
                super(My_T, self).was_mounted()

        defaulttext = My_T('Hello world')
        default_p = My_C('p', [defaulttext])
        defaultroute = My_C('div', [default_p])

        assert counter['count'] == 0

        r = Router({ }, defaultroute, js.globals.document.body)
        r.route()

        assert counter['count'] == 1 * 3

        defaultroute.attribs = {'class': 'stuff'}
        defaultroute.mount_redraw()

        assert counter['count'] == 2 * 3

        defaulttext.text = 'Hello world2'
        defaultroute.mount_redraw()

        assert counter['count'] == 3 * 3

