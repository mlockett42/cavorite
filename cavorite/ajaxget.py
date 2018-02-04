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

global_cavorite_ajaxgethandler = None
global_cavorite_ajaxposthandler = None

def initialise_ajaxget_callbacks():
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


