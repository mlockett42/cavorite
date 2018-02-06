# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import tests.fakejs as js
import cavorite.cavorite

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

