import collections
import functools
import re
from collections import namedtuple
from copy import deepcopy
from enum import Enum
from string import Template as PyTemplate
from typing import Any

_sentinel_dict = {}


# pylint: disable=dangerous-default-value
# We use the fact that a default of a dict type is static in order to detect if
# the __mapping variable was not passed.
class Template:
    patter_str = r"\$(?:(?P<escaped>\$)|{(?P<braced>.+?)}|(?P<invalid>))"

    def __init__(self, template):
        self.pattern: re.Pattern = re.compile(self.patter_str, re.VERBOSE)
        self.template = template

    def substitute(self, __mapping=_sentinel_dict, /, **kwds) -> str:
        # Using the fact that a default dict is a fixed object to detect if an
        # unnamed mapping dictioanry was passed in.
        mapping = self._mapping(__mapping, **kwds)
        mapping = named_tuple_from_dict("mapping", mapping)

        def convert(match_object):
            # Explicitely use `mapping` in this closure, otherwise the implicite
            # use in eval won't work
            mapping  # pylint: disable=pointless-statement

            if expression := match_object.group("braced"):
                f_string = rf'f"{{mapping.{expression}}}"'
                return eval(f_string)  # pylint: disable=eval-used
            if expression := match_object.group("escaped"):
                return "$"
            if expression := match_object.group("invalid"):
                return match_object.group()
            raise LookupError(
                f"Unexpected match group in {match_object.group()}"
            )

        return self.pattern.sub(convert, self.template)

    def safe_substitute(self, __mapping=_sentinel_dict, /, **kwds) -> str:
        # Using the fact that a default dict is a fixed object to detect if an
        # unnamed mapping dictioanry was passed in.
        mapping = self._mapping(__mapping, **kwds)
        mapping = named_tuple_from_dict("mapping", mapping)

        def convert(match_object):
            # Explicitely use `mapping` in this closure, otherwise the implicite
            # use in eval won't work
            mapping  # pylint: disable=pointless-statement

            if expression := match_object.group("braced"):
                f_string = rf'f"{{mapping.{expression}}}"'
                try:
                    return eval(f_string)  # pylint: disable=eval-used
                except Exception:  # pylint: disable=broad-exception-caught
                    return match_object.group()
            if expression := match_object.group("escaped"):
                return "$"
            if expression := match_object.group("invalid"):
                return match_object.group()
            raise LookupError(
                f"Unexpected match group in {match_object.group()}"
            )

        return self.pattern.sub(convert, self.template)

    def _mapping(self, __mapping=_sentinel_dict, /, **kwds) -> dict[str, Any]:
        assert isinstance(__mapping, dict)
        assert isinstance(kwds, dict)

        if __mapping is _sentinel_dict:
            mapping = kwds
        else:
            mapping = _merge(__mapping, kwds)
        return mapping


def named_tuple_from_dict(name: str, dictionary: dict[str, Any]):
    assert isinstance(dictionary, collections.abc.MutableMapping)

    for k, v in dictionary.items():
        if isinstance(v, collections.abc.MutableMapping):
            dictionary[k] = named_tuple_from_dict(k, v)

    new_tuple = namedtuple(name, dictionary)
    tuple_obj = new_tuple(**dictionary)
    return tuple_obj


def _merge(a, b):
    for k, vb in b.items():
        if va := a.get(k):
            if isinstance(vb, collections.abc.MutableMapping) and isinstance(
                va, collections.abc.MutableMapping
            ):
                _merge(va, vb)
            else:
                a[k] = b[k]
        else:
            a[k] = b[k]
    return a
