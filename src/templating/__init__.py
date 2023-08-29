import collections
from collections.abc import Mapping
from string import Template as PyTemplate

_sentinel_dict = {}


# pylint: disable=dangerous-default-value
class Template(PyTemplate):
    braceidpattern = r"(?a:[_a-z][_a-z0-9\.]*)"

    def substitute(self, __mapping=_sentinel_dict, /, **kwds) -> str:
        # Using the fact that a default dict is a fixed object to detect if an
        # un named mapping dictioanry was passed in.
        assert isinstance(__mapping, dict)
        assert isinstance(kwds, dict)

        if __mapping is _sentinel_dict:
            mapping = _flatten(kwds)
        else:
            mapping = _flatten(__mapping) | _flatten(kwds)

        return super().substitute(mapping)


def _flatten(obj, parent_key=None, separator="."):
    if isinstance(obj, collections.abc.MutableMapping):
        return _flatten_dict(obj, parent_key, separator)
    if isinstance(obj, list):
        return _flatten_list(obj, parent_key, separator)
    if hasattr(obj, "__dict__"):
        return _flatten_dict(obj.__dict__, parent_key, separator)
    return {parent_key: str(obj)}


def _flatten_dict(dictionary, parent_key, separator):
    assert isinstance(dictionary, collections.abc.MutableMapping)
    items = {}
    for key, value in dictionary.items():
        new_key = key if parent_key is None else f"{parent_key}{separator}{key}"
        items |= _flatten(value, new_key, separator)
    return dict(items)


def _flatten_list(values, parent_key, separator):
    assert isinstance(values, list)
    items = {}
    for i, v in enumerate(values):
        new_key = (
            str(i) if parent_key is None else f"{parent_key}{separator}{str(i)}"
        )
        items |= _flatten(v, new_key, separator)
    return items
