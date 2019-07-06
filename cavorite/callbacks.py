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
                            'onmouseup', 'onsubmit', 'onkeyup', 'onkeydown',
                            'onkeypress'
                            }

global_callback_handlers = { k: None for k in supported_callback_names }

def initialise_global_callbacks():
    #TODO: These callbacks contain a lot of repeated code. It should go in some functions
    # initialise callbacks for commonly used handlers
    global global_callbacks
    global supported_callback_names
    global_callbacks = { k: dict() for k in supported_callback_names }

    @output_exceptions
    def local_onclick_handler(e):
        #print('local_onclick_handler called')
        global global_callbacks
        callbacks = global_callbacks['onclick']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)

    global global_callback_handlers
    global_callback_handlers['onclick'] = local_onclick_handler

    @output_exceptions
    def local_onchange_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onchange']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onchange'] = local_onchange_handler

    @output_exceptions
    def local_oncontextmenu_handler(e):
        global global_callbacks
        callbacks = global_callbacks['oncontextmenu']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['oncontextmenu'] = local_oncontextmenu_handler

    @output_exceptions
    def local_ondblclick_handler(e):
        global global_callbacks
        callbacks = global_callbacks['ondblclick']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['ondblclick'] = local_ondblclick_handler

    @output_exceptions
    def local_onmousedown_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmousedown']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmousedown'] = local_onmousedown_handler

    @output_exceptions
    def local_onmouseenter_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmouseenter']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmouseenter'] = local_onmouseenter_handler

    @output_exceptions
    def local_onmouseleave_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmouseleave']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmouseleave'] = local_onmouseleave_handler

    @output_exceptions
    def local_onmousemove_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmousemove']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmousemove'] = local_onmousemove_handler

    @output_exceptions
    def local_onmouseover_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmouseover']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmouseover'] = local_onmouseover_handler

    @output_exceptions
    def local_onmouseup_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onmouseup']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onmouseup'] = local_onmouseup_handler

    @output_exceptions
    def local_onsubmit_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onsubmit']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onsubmit'] = local_onsubmit_handler

    @output_exceptions
    def local_onkeydown_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onkeydown']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onkeydown'] = local_onsubmit_handler

    @output_exceptions
    def local_onkeydown_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onkeyup']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onkeyup'] = local_onsubmit_handler

    @output_exceptions
    def local_onkeydown_handler(e):
        global global_callbacks
        callbacks = global_callbacks['onkeypress']
        target = e.target
        cavorite_id = str(target.getAttribute('_cavorite_id'))
        if cavorite_id in callbacks and callbacks[cavorite_id] is not None:
            callbacks[cavorite_id](e)
    global_callback_handlers['onkeypress'] = local_onsubmit_handler
