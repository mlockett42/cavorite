# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
try:
    import js
except ImportError:
    js = None
from . import get_uuid
import uuid

global_ajaxget_callbacks = None
global_ajaxpost_callbacks = None
global_ajaxput_callbacks = None
global_ajaxdelete_callbacks = None
global_cavorite_ajaxgethandler = None
global_cavorite_ajaxposthandler = None
global_cavorite_ajaxputhandler = None
global_cavorite_ajaxdeletehandler = None

def initialise_ajaxget_callbacks():
    # Initialise GET, POST, PUT and DELETE handlers
    # Each handler has it's own dict of callback functions
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

    # Initialise DELETE handlers
    global global_ajaxdelete_callbacks
    global_ajaxdelete_callbacks = dict()

    @js.Function
    def cavorite_ajaxdeletehandler(xmlhttp, key, response):
        key = str(key)
        global global_ajaxdelete_callbacks

        global_ajaxdelete_callbacks[key](xmlhttp, response)

        del global_ajaxdelete_callbacks[key]

    js.globals.document.cavorite_AjaxDeleteCallback = cavorite_ajaxdeletehandler

    global global_cavorite_ajaxdeletehandler
    global_cavorite_ajaxdeletehandler = cavorite_ajaxdeletehandler


def ajaxget(url, handler_fn):
    # Called be application code to execute an AJAX GET request
    # Sets up the callback and then calls into the javascript
    global global_ajaxget_callbacks
    function_id = str(get_uuid())

    global_ajaxget_callbacks[function_id] = handler_fn

    val = js.globals.cavorite_ajaxGet(url, function_id)

def ajaxpost(url, data, handler_fn):
    # Called be application code to execute an AJAX GET request
    # Sets up the callback and then calls into the javascript
    global global_ajaxpost_callbacks
    function_id = str(get_uuid())

    global_ajaxpost_callbacks[function_id] = handler_fn

    val = js.globals.cavorite_ajaxPost(url, function_id, data)

def ajaxput(url, data, handler_fn):
    # Called be application code to execute an AJAX GET request
    # Sets up the callback and then calls into the javascript
    global global_ajaxput_callbacks
    function_id = str(get_uuid())

    global_ajaxput_callbacks[function_id] = handler_fn

    val = js.globals.cavorite_ajaxPut(url, function_id, data)

def ajaxdelete(url, handler_fn):
    # Called be application code to execute an AJAX GET request
    # Sets up the callback and then calls into the javascript
    global global_ajaxdelete_callbacks
    function_id = str(get_uuid())

    global_ajaxdelete_callbacks[function_id] = handler_fn

    val = js.globals.cavorite_ajaxDelete(url, function_id)


