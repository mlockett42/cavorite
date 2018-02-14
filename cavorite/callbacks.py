# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
try:
    import js
except ImportError:
    js = None

global_callbacks = None

supported_callback_names = {'onclick', 'onchange', 'oncontextmenu'}

#global_callback_handlers = {'onclick': None, 'onchange': None}
global_callback_handlers = { k: None for k in supported_callback_names }

def initialise_global_callbacks():
    global global_callbacks
    global supported_callback_names
    #global_callbacks = { 'onclick': dict(), 'onchange': dict(), }
    global_callbacks = { k: dict() for k in supported_callback_names }

    """
    @js.Function
    def local_onclick_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onclick']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global global_callback_handlers
    global_callback_handlers['onclick'] = local_onclick_handler

    @js.Function
    def local_onchange_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onchange']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['onchange'] = local_onchange_handler
    """

    for k in global_callbacks:
        @js.Function
        def local_event_handler(e):
            callbacks = global_callbacks[k]
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        global_callback_handlers[k] = local_event_handler

    #print('initialise_global_callbacks global_callback_handlers=', global_callback_handlers)
