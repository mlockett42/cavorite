# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
try:
    import js
except ImportError:
    js = None
import sys
import traceback


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
    def local_onclick_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['onclick']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            #exc_info = sys.exc_info()
            #(exc_type, exc_value, exc_traceback) = exc_info
            #print('Inner exception exc_type=',exc_type)
            #print('Error message')
            #print(err.message)
            print("Exception")
            #print('Inner exception exc_value=',exc_value)
            #print('Inner exception exc_traceback=',exc_traceback)
            #print('Inner exception extract_tb=',traceback.extract_tb(exc_traceback))
            #print('dir(err)',dir(err))
            #print('exc_traceback=',exc_traceback)
            #print('err.trace=', err.trace)
            traceback.print_exc(file=sys.stdout)
            #del exc_info
            raise
    global global_callback_handlers
    global_callback_handlers['onclick'] = local_onclick_handler

    @js.Function
    def local_onchange_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['onchange']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['onchange'] = local_onchange_handler

    @js.Function
    def local_oncontextmenu_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['oncontextmenu']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['oncontextmenu'] = local_oncontextmenu_handler

    @js.Function
    def local_ondblclick_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['ondblclick']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['ondblclick'] = local_ondblclick_handler

    @js.Function
    def local_onmousedown_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['onmousedown']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['onmousedown'] = local_onmousedown_handler

    @js.Function
    def local_onmouseenter_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['onmouseenter']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['onmouseenter'] = local_onmouseenter_handler

    @js.Function
    def local_onmouseleave_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['onmouseleave']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['onmouseleave'] = local_onmouseleave_handler

    @js.Function
    def local_onmousemove_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['onmousemove']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['onmousemove'] = local_onmousemove_handler

    @js.Function
    def local_onmouseover_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['onmouseover']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['onmouseover'] = local_onmouseover_handler

    @js.Function
    def local_onmouseup_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['onmouseup']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['onmouseup'] = local_onmouseup_handler

    @js.Function
    def local_onsubmit_handler(e):
        try:
            global global_callbacks
            callbacks = global_callbacks['onsubmit']
            target = e.target
            cavorite_id = str(target.getAttribute('_cavorite_id'))
            if cavorite_id in callbacks:
                callbacks[cavorite_id](e)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise
    global_callback_handlers['onsubmit'] = local_onsubmit_handler
