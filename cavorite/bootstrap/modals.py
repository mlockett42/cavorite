# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from ..HTML import *
import copy
from .. import get_current_hash
try:
    import js
except ImportError:
    js = None


class ModalTrigger(a):
    def __init__(self, attribs, children, target):
        attribs = copy.copy(attribs)
        attribs.update({'data-toggle': "modal", 'data-target': target, 'href': get_current_hash()})
        super(ModalTrigger, self).__init__(attribs, children)



class Modal(div):
    def __init__(self, id, title, body, onclickhandler):
        self.id = id
        self.title = title
        self.body = body
        self.onclickhandler = onclickhandler
        def handle_ok2(e):
            jquery = js['$']
            jquery('#' + id).modal('hide')
        self.handle_ok2 = handle_ok2
        super(Modal, self).__init__({'class': "modal fade", "id":id, "tabindex": "-1", "role": "dialog", "aria-labeledby": "{}Label".format(id), "aria-hidden": "true"})

    def handle_ok(self, e):
        def IterateElements(node, callback):
            callback(node)
            for i in range(node.children.length):
                child = node.children.item(i)
                IterateElements(child, callback)

        control_values = dict()

        def control_values_callback(node):
            if hasattr(node, 'tagName'):
                if (str(node.tagName).lower() == 'input' or str(node.tagName).lower() == 'select'):
                    if node.getAttribute('type') == 'checkbox':
                        control_values[str(node.getAttribute('id'))] = node.checked
                    else:
                        control_values[str(node.getAttribute('id'))] = node.value

        if self.onclickhandler is not None:
            IterateElements(js.document.getElementById(self.id), control_values_callback)
            self.onclickhandler(e, control_values)
        jquery = js.jquery
        jquery('#' + self.id).modal('hide')

    def get_children(self):
        return  [
                  div({'class': "modal-dialog", "role": "document"}, [
                    div({'class': 'modal-content'}, [
                      div({'class': 'modal-header'}, [
                        h5({'class': 'modal-title', 'id':  "{}Label".format(self.id)}, self.title),
                        html_button({'type': 'button', 'class': 'close', 'data-dismiss': 'modal', 'aria-label': 'Close'}, [
                          span({'aria-hidden': 'true'}, 'X'),
                        ]),
                      ]),
                      div({'class': 'modal-body'}, [
                        form(self.body)
                      ]),
                      div({'class': 'modal-footer'}, [
                        html_button({'type': "button", 'class':"btn btn-secondary", 'data-dismiss':"modal"}, 'Cancel'),
                        html_button({'type': "button", 'class':"btn btn-primary", 'onclick': self.handle_ok}, 'OK'),
                      ]),
                    ]),
                  ]),
                ]
