# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
try:
    import js
except ImportError:
    js = None

global_callbacks = None

global_onclick_handler = None

def initialise_global_callbacks():
    global global_callbacks
    global_callbacks = {'onclick': dict() }

    @js.Function
    def local_onclick_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onclick']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global global_onclick_handler
    global_onclick_handler = local_onclick_handler


