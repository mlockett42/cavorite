# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
try:
    import js
except ImportError:
    js = None
from .exceptions import output_exceptions


global_callbacks = None

supported_callback_names = {'onclick', 'onchange', 'oncontextmenu',
                            'ondblclick', 'onmousedown', 'onmouseenter',
                            'onmouseleave', 'onmousemove', 'onmouseover',
                            'onmouseup', 'onsubmit',
                            }

global_callback_handlers = { k: None for k in supported_callback_names }

def initialise_global_callbacks():
    #TODO: These callbacks contain a lot of repeated code. It should go in some functions
    # initialise callbacks for commonly used handlers
    global global_callbacks
    global supported_callback_names
    global_callbacks = { k: dict() for k in supported_callback_names }

    @js.Function
    @output_exceptions
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
    @output_exceptions
    def local_onchange_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onchange']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['onchange'] = local_onchange_handler

    @js.Function
    @output_exceptions
    def local_oncontextmenu_handler(e):
        global global_callbacks
        callbacks = global_callbacks['oncontextmenu']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['oncontextmenu'] = local_oncontextmenu_handler

    @js.Function
    @output_exceptions
    def local_ondblclick_handler(e):
        global global_callbacks
        callbacks = global_callbacks['ondblclick']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['ondblclick'] = local_ondblclick_handler

    @js.Function
    @output_exceptions
    def local_onmousedown_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmousedown']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmousedown'] = local_onmousedown_handler

    @js.Function
    @output_exceptions
    def local_onmouseenter_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmouseenter']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmouseenter'] = local_onmouseenter_handler

    @js.Function
    @output_exceptions
    def local_onmouseleave_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmouseleave']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmouseleave'] = local_onmouseleave_handler

    @js.Function
    @output_exceptions
    def local_onmousemove_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmousemove']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmousemove'] = local_onmousemove_handler

    @js.Function
    @output_exceptions
    def local_onmouseover_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmouseover']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmouseover'] = local_onmouseover_handler

    @js.Function
    @output_exceptions
    def local_onmouseup_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmouseup']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmouseup'] = local_onmouseup_handler

    @js.Function
    @output_exceptions
    def local_onsubmit_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onsubmit']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks:
            callbacks[cavorite_id](e)
    global_callback_handlers['onsubmit'] = local_onsubmit_handler
