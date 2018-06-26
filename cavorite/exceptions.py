from __future__ import absolute_import, unicode_literals, print_function
import traceback
import sys


def output_exceptions(func):
    # Wrap the given function and print the exception to the console
    # This gives us a good error report when there is an exception inside
    # a pypyjs event handler. Otherwise only and error message no stack
    # trace or even line number
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as err:
            # Print the exception info because by default we don't get that
            # in pypyjs event handlers
            print("Exception")
            traceback.print_exc(file=sys.stdout)
            raise

    return wrapper
