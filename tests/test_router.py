# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import tests.fakejs as js
import cavorite.cavorite
from mock import Mock

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

        error_404_page = c("div", [c("p", "No match 404 error"),
                                   c("p", [c("a", {"href": "/#!"}, "Back to main page")])])

        r = Router({r'^$': welcome_page,
                    r'^hello$': hello_page},
                    error_404_page, body)
        r.route()

        r.on_body_click(Mock())

        welcome_page.on_body_click.assert_called()

        hello_page.on_body_click.assert_not_called()

        

