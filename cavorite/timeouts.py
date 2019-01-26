# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
try:
    import js
except ImportError:
    js = None
from . import get_uuid
import uuid
from .exceptions import output_exceptions

global_timeout_callbacks = None
global_timeout_val_to_id = None
global_timeout_id_to_val = None

global_interval_callbacks = None
global_interval_val_to_id = None
global_interval_id_to_val = None

global_cavorite_timeouthandler = None
global_cavorite_intervalhandler = None

def initialise_timeout_callbacks():
    global global_timeout_callbacks
    global_timeout_callbacks = dict()
    global global_timeout_val_to_id
    global_timeout_val_to_id = dict()
    global global_timeout_id_to_val
    global_timeout_id_to_val = dict()

    global global_interval_callbacks
    global_interval_callbacks = dict()
    global global_interval_val_to_id
    global_interval_val_to_id = dict()
    global global_interval_id_to_val
    global_interval_id_to_val = dict()

    @js.Function
    @output_exceptions
    def cavorite_timeouthandler(key):
        key = str(key)
        global global_timeout_callbacks
        global global_timeout_val_to_id
        global global_timeout_id_to_val

        global_timeout_callbacks[key]()

        val = global_timeout_id_to_val[key]
        del global_timeout_callbacks[key]
        del global_timeout_id_to_val[key]
        del global_timeout_val_to_id[val]

    js.globals.document.cavorite_timeouthandler = cavorite_timeouthandler

    global global_cavorite_timeouthandler
    global_cavorite_timeouthandler = cavorite_timeouthandler

    @js.Function
    @output_exceptions
    def cavorite_intervalhandler(key):
        key = str(key)
        global global_interval_callbacks
        global global_interval_val_to_id
        global global_interval_id_to_val

        global_interval_callbacks[str(key)]()

    js.globals.document.cavorite_intervalhandler = cavorite_intervalhandler

    global global_cavorite_intervalhandler
    global_cavorite_intervalhandler = cavorite_intervalhandler

def set_timeout(handler_fn, delay):
    global global_timeout_callbacks
    function_id = str(get_uuid())

    global_timeout_callbacks[function_id] = handler_fn

    val = js.globals.cavorite_setTimeout(function_id, delay)

    global global_timeout_val_to_id
    global global_timeout_id_to_val

    global_timeout_val_to_id[val] = function_id
    global_timeout_id_to_val[function_id] = val

    return val

def clear_timeout(val):
    global global_timeout_val_to_id
    global global_timeout_id_to_val
    global global_timeout_callbacks

    js.globals.clearTimeout(val)

    if val in global_timeout_val_to_id:
        # Sometimes we appear to can called the clear a timeout that someone
        # has already cleared
        function_id = global_timeout_val_to_id[val]

        del global_timeout_val_to_id[val]
        del global_timeout_id_to_val[function_id]
        del global_timeout_callbacks[function_id]

def set_interval(handler_fn, delay):
    global global_interval_callbacks
    function_id = str(get_uuid())

    global_interval_callbacks[function_id] = handler_fn

    val = js.globals.cavorite_setInterval(function_id, delay)

    global global_interval_val_to_id
    global global_interval_id_to_val

    global_interval_val_to_id[val] = function_id
    global_interval_id_to_val[function_id] = val

    return val

def clear_interval(val):
    global global_interval_val_to_id
    global global_interval_id_to_val
    global global_interval_callbacks

    js.globals.clearInterval(val)

    if val in global_interval_val_to_id:
        # Sometimes we appear to can called the clear a timeout that someone
        # has already cleared
        function_id = global_interval_val_to_id[val]

        del global_interval_val_to_id[val]
        del global_interval_id_to_val[function_id]
        del global_interval_callbacks[function_id]
