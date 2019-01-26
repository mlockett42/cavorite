# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import tests.fakejs as js
import cavorite.cavorite
from mock import Mock
from cavorite.cavorite.HTML import *

Router = cavorite.cavorite.Router
c = cavorite.cavorite.c
t = cavorite.cavorite.t


class TestRouter(object):
    def test_router_stores_statically(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)

        body = js.globals.document.body

        welcome_page = c("div", [c("p", "Welcome to cavorite"),
                                 ])

        error_404_page = c("div", [c("p", "No match 404 error"),
                                   c("p", [c("a", {"href": "/#!"}, "Back to main page")])])

        r = Router({r'^$': welcome_page},
                    error_404_page, body)
        #r.route()

        assert Router.router == r

    def test_router_passes_body_clicks_to_view(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)

        body = js.globals.document.body

        welcome_page = c("div", [c("p", "Welcome to cavorite"),
                                 ])

        hello_page = c("div", [c("p", "Hello there"),
                                 ])

        welcome_page.on_body_click = Mock()
        hello_page.on_body_click = Mock()

        welcome_page.on_body_mousemove = Mock()
        hello_page.on_body_mousemove = Mock()

        welcome_page.on_body_keyup = Mock()
        hello_page.on_body_keyup = Mock()

        welcome_page.on_body_keydown = Mock()
        hello_page.on_body_keydown = Mock()

        welcome_page.on_body_keypress = Mock()
        hello_page.on_body_keypress = Mock()

        error_404_page = c("div", [c("p", "No match 404 error"),
                                   c("p", [c("a", {"href": "/#!"}, "Back to main page")])])

        r = Router({r'^$': welcome_page,
                    r'^hello$': hello_page},
                    error_404_page, body)
        r.route()

        r.on_body_click(Mock())

        welcome_page.on_body_click.assert_called()

        hello_page.on_body_click.assert_not_called()

        r.on_body_mousemove(Mock(clientX=500, clientY=510))

        welcome_page.on_body_mousemove.assert_called()

        hello_page.on_body_mousemove.assert_not_called()

        r.on_body_keyup(Mock())

        welcome_page.on_body_keyup.assert_called()

        hello_page.on_body_keyup.assert_not_called()

        r.on_body_keydown(Mock())

        welcome_page.on_body_keydown.assert_called()

        hello_page.on_body_keydown.assert_not_called()

        r.on_body_keypress(Mock())

        welcome_page.on_body_keypress.assert_called()

        hello_page.on_body_keypress.assert_not_called()


    def test_router_handles_global_mousemove(self, monkeypatch):
        monkeypatch.setattr(cavorite.cavorite, 'js', js)

        body = js.globals.document.body

        welcome_page = c("div", [c("p", "Welcome to cavorite"),
                                 ])

        hello_page = c("div", [c("p", "Hello there"),
                                 ])

        welcome_page.on_body_click = Mock()

        error_404_page = c("div", [c("p", "No match 404 error"),
                                   c("p", [c("a", {"href": "/#!"}, "Back to main page")])])

        r = Router({r'^$': welcome_page,
                    },
                    error_404_page, body)
        r.route()

        r.on_body_mousemove(Mock(clientX=500, clientY=500))

        assert r.global_mouse_x == 500
        assert r.global_mouse_y == 500

        welcome_page.on_body_mousemove = Mock()

        r.on_body_mousemove(Mock(clientX=520, clientY=530))

        args = welcome_page.on_body_mousemove.call_args
        assert args[0][1] == 20
        assert args[0][2] == 30

        assert r.global_mouse_x == 520
        assert r.global_mouse_y == 530

    def test_router_handles_routes_which_are_callables(self, monkeypatch):
        class EditorView(div):
            def get_children(self):
                return [p(str(self.get_root().url_kwargs['project_id']))]

        monkeypatch.setattr(cavorite.cavorite, 'js', js)

        body = js.globals.document.body

        js.globals.window.location.href = '#!editor/d8fb8497-fb86-4dea-bd9c-49ad883b7a84'

        def editor_page():
            return EditorView()

        hello_page = c("div", [c("p", "Hello there"),
                                 ])

        error_404_page = c("div", [c("p", "No match 404 error"),
                                   c("p", [c("a", {"href": "/#!"}, "Back to main page")])])

        r = Router({r'^editor/(?P<project_id>[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})$': editor_page,
                    },
                    error_404_page, body)
        r.route()

        div1 = body.children.item(0)
        assert div1.tagName == 'div'
        assert div1.children.length == 1
        p1 = div1.children.item(0)
        assert p1.children.length == 1
        assert str(p1.children.item(0)) == 'd8fb8497-fb86-4dea-bd9c-49ad883b7a84'
