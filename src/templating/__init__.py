import collections
import re
from enum import Enum
from string import Template as PyTemplate

_sentinel_dict = {}


# pylint: disable=dangerous-default-value
class Template(PyTemplate):
    braceidpattern = r"(?a:[_a-z][_a-z0-9\.]*)"

    def substitute(self, __mapping=_sentinel_dict, /, **kwds) -> str:
        # Using the fact that a default dict is a fixed object to detect if an
        # un named mapping dictioanry was passed in.
        mapping = self._mapping(__mapping, **kwds)

        result = super().substitute(mapping)
        if result != self.template:
            if re.search(r"\${", result):
                result = re.sub(r"\$([^{])", r"$$\1", result)
                t = Template(result)
                result = t.substitute(mapping)
        return result

    def safe_substitute(self, __mapping=_sentinel_dict, /, **kwds) -> str:
        # Using the fact that a default dict is a fixed object to detect if an
        # un named mapping dictioanry was passed in.
        mapping = self._mapping(__mapping, **kwds)

        result = super().safe_substitute(mapping)
        if result != self.template:
            t = Template(result)
            result = t.safe_substitute(mapping)
        return result

    def _mapping(self, __mapping=_sentinel_dict, /, **kwds):
        assert isinstance(__mapping, dict)
        assert isinstance(kwds, dict)

        if __mapping is _sentinel_dict:
            mapping = _flatten(kwds)
        else:
            mapping = _flatten(__mapping) | _flatten(kwds)
        return mapping


def _flatten(obj, parent_key=None, separator="."):
    if isinstance(obj, collections.abc.MutableMapping):
        return _flatten_dict(obj, parent_key, separator)
    if isinstance(obj, list):
        return _flatten_list(obj, parent_key, separator)
    if isinstance(obj, Enum):
        return {parent_key: str(obj)}
    if hasattr(obj, "__dict__"):
        return _flatten_dict(obj.__dict__, parent_key, separator)
    return {parent_key: str(obj)}


def _flatten_dict(dictionary, parent_key, separator):
    assert isinstance(dictionary, collections.abc.MutableMapping)
    items = {}
    for key, value in dictionary.items():
        if key == "parent":
            continue
        new_key = key if parent_key is None else f"{parent_key}{separator}{key}"
        items |= _flatten(value, new_key, separator)
    return items


def _flatten_list(values, parent_key, separator):
    assert isinstance(values, list)
    items = {}
    for i, v in enumerate(values):
        new_key = (
            str(i) if parent_key is None else f"{parent_key}{separator}{str(i)}"
        )
        items |= _flatten(v, new_key, separator)
    return items
