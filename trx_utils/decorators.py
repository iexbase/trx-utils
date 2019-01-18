# --------------------------------------------------------------------
# Copyright (c) iEXBase. All rights reserved.
# Licensed under the MIT License.
# See License.txt in the project root for license information.
# --------------------------------------------------------------------

import functools
import itertools
import threading
import warnings

from typing import Any, Callable, Dict

from .types import is_text


class combomethod(object):
    def __init__(self, method):
        self.method = method

    def __get__(self, obj=None, objtype=None):
        @functools.wraps(self.method)
        def _wrapper(*args, **kwargs):
            if obj is not None:
                return self.method(obj, *args, **kwargs)
            else:
                return self.method(objtype, *args, **kwargs)

        return _wrapper


def reject_recursive_repeats(to_wrap):
    """Prevent simple cycles by returning None when called recursively with same instance"""
    to_wrap.__already_called = {}

    @functools.wraps(to_wrap)
    def wrapped(*args):
        arg_instances = tuple(map(id, args))
        thread_id = threading.get_ident()
        thread_local_args = (thread_id,) + arg_instances
        if thread_local_args in to_wrap.__already_called:
            raise ValueError('Recursively called %s with %r' % (to_wrap, args))
        to_wrap.__already_called[thread_local_args] = True
        try:
            wrapped_val = to_wrap(*args)
        finally:
            del to_wrap.__already_called[thread_local_args]
        return wrapped_val

    return wrapped


def deprecated_for(replace_message):
    """
    Decorate a deprecated function, with info about what to use instead, like:

    Examples:
        >>> @deprecated_for("toBytes()")
        >>> def toAscii(arg):
    """

    def decorator(to_wrap):
        @functools.wraps(to_wrap)
        def wrapper(*args, **kwargs):
            warnings.warn(
                "%s is deprecated in favor of %s" % (to_wrap.__name__, replace_message),
                category=DeprecationWarning,
                stacklevel=2)
            return to_wrap(*args, **kwargs)

        return wrapper

    return decorator


def validate_conversion_arguments(to_wrap):
    """
    Validates arguments for conversion functions.
    - Only a single argument is present
    - Kwarg must be 'primitive' 'hexstr' or 'text'
    - If it is 'hexstr' or 'text' that it is a text type
    """

    @functools.wraps(to_wrap)
    def wrapper(*args, **kwargs):
        _assert_one_val(*args, **kwargs)
        if kwargs:
            _validate_supported_kwarg(kwargs)

        if len(args) is 0 and "primitive" not in kwargs:
            _assert_hexstr_or_text_kwarg_is_text_type(**kwargs)
        return to_wrap(*args, **kwargs)

    return wrapper


def _validate_supported_kwarg(kwargs):
    if next(iter(kwargs)) not in ["primitive", "hexstr", "text"]:
        raise TypeError(
            "Kwarg must be 'primitive', 'hexstr', or 'text'. "
            "Instead, kwarg was: %r" % (next(iter(kwargs)))
        )


def _assert_one_val(*args, **kwargs):
    if not _has_one_val(*args, **kwargs):
        raise TypeError(
            "Exactly one of the passed values can be specified. "
            "Instead, values were: %r, %r" % (args, kwargs)
        )


def _has_one_val(*args, **kwargs):
    vals = itertools.chain(args, kwargs.values())
    not_nones = list(filter(lambda val: val is not None, vals))
    return len(not_nones) == 1


def _assert_hexstr_or_text_kwarg_is_text_type(**kwargs):
    if not _hexstr_or_text_kwarg_is_text_type(**kwargs):
        raise TypeError(
            "Arguments passed as hexstr or text must be of text type. "
            "Instead, value was: %r" % (repr(next(list(kwargs.values()))))
        )


def _hexstr_or_text_kwarg_is_text_type(**kwargs):
    value = kwargs["hexstr"] if "hexstr" in kwargs else kwargs["text"]
    return is_text(value)
