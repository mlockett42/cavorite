# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
try:
    import js
except ImportError:
    js = None

def get_uuid():
    return uuid.uuid4()

import uuid

global_ajaxget_callbacks = None
global_ajaxpost_callbacks = None
global_ajaxput_callbacks = None

global_cavorite_ajaxgethandler = None
global_cavorite_ajaxposthandler = None
global_cavorite_ajaxputhandler = None

def initialise_ajaxget_callbacks():
    # Initialise GET handlers
    global global_ajaxget_callbacks
    global_ajaxget_callbacks = dict()

    @js.Function
    def cavorite_ajaxgethandler(xmlhttp, key, response):
        key = str(key)
        global global_ajaxget_callbacks

        global_ajaxget_callbacks[key](xmlhttp, response)

        del global_ajaxget_callbacks[key]

    js.globals.document.cavorite_AjaxGetCallback = cavorite_ajaxgethandler

    global global_cavorite_ajaxgethandler
    global_cavorite_ajaxgethandler = cavorite_ajaxgethandler

    # Initialise POST handlers
    global global_ajaxpost_callbacks
    global_ajaxpost_callbacks = dict()

    @js.Function
    def cavorite_ajaxposthandler(xmlhttp, key, response):
        key = str(key)
        global global_ajaxpost_callbacks

        global_ajaxpost_callbacks[key](xmlhttp, response)

        del global_ajaxpost_callbacks[key]

    js.globals.document.cavorite_AjaxPostCallback = cavorite_ajaxposthandler

    global global_cavorite_ajaxposthandler
    global_cavorite_ajaxposthandler = cavorite_ajaxposthandler

    # Initialise PUT handlers
    global global_ajaxput_callbacks
    global_ajaxput_callbacks = dict()

    @js.Function
    def cavorite_ajaxputhandler(xmlhttp, key, response):
        key = str(key)
        global global_ajaxput_callbacks

        global_ajaxput_callbacks[key](xmlhttp, response)

        del global_ajaxput_callbacks[key]

    js.globals.document.cavorite_AjaxPutCallback = cavorite_ajaxputhandler

    global global_cavorite_ajaxputhandler
    global_cavorite_ajaxputhandler = cavorite_ajaxputhandler


def ajaxget(url, handler_fn):
    global global_ajaxget_callbacks
    function_id = str(get_uuid())

    global_ajaxget_callbacks[function_id] = handler_fn

    val = js.globals.cavorite_ajaxGet(url, function_id)

def ajaxpost(url, data, handler_fn):
    global global_ajaxpost_callbacks
    function_id = str(get_uuid())

    global_ajaxpost_callbacks[function_id] = handler_fn

    val = js.globals.cavorite_ajaxPost(url, function_id, data)

def ajaxput(url, data, handler_fn):
    global global_ajaxput_callbacks
    function_id = str(get_uuid())

    global_ajaxput_callbacks[function_id] = handler_fn

    val = js.globals.cavorite_ajaxPut(url, function_id, data)


