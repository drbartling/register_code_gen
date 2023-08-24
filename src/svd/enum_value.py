import logging
import re
from typing import List, Optional, Union

from pydantic.dataclasses import dataclass

from svd.usage import Usage

_logger = logging.getLogger(__name__)


@dataclass
class Field:
    pass


@dataclass
class EnumeratedValues:
    parent: Optional["Field"]
    derived_from: Optional["EnumeratedValues"]
    name: Optional[str]
    header_enum_name: Optional[str]
    usage: Optional[Usage]
    enumerated_values: List["EnumeratedValue"]

    def __iter__(self):
        yield from self.enumerated_values

    @classmethod
    def from_dict(cls, enum_dict):
        new_cls = cls(
            parent=enum_dict.get("parent"),
            derived_from=enum_dict.get("derivedFrom"),
            name=enum_dict.get("name"),
            header_enum_name=enum_dict.get("headerEnumName"),
            usage=enum_dict.get("usage", Usage.READ_WRITE),
            enumerated_values=[
                EnumeratedValue.from_dict(ev)
                for ev in enum_dict.get("enumeratedValue")
            ],
        )
        for ev in new_cls:
            ev.parent = new_cls
        return new_cls


@dataclass
class EnumeratedValue:
    parent: Optional[EnumeratedValues]
    name: Optional[str]
    description: Optional[str]
    value: Optional[Union[int, str]]
    is_default: Optional[bool]

    def __post_init__(self):
        self._parse_value()

    def _parse_value(self):
        if not isinstance(self.value, str):
            return

        self.value = self.value.strip()

        hex_str = re.match(r"0x([0-9a-fA-F]+)\b", self.value)
        if hex_str:
            value = hex_str.groups()[0]
            self.value = int(value, 16)
            return

        bin_str = re.match(r"0b([0-1x]+)\b", self.value) or re.match(
            r"#([0-1x]+)\b", self.value
        )
        if bin_str:
            value = bin_str.groups()[0]
            value = value.replace("x", "0")
            self.value = int(value, 2)
            return

        err_msg = f"Failed to parse {self.value} as integer"
        _logger.error(err_msg)
        raise ValueError(err_msg)

    @classmethod
    def from_dict(cls, enum_dict, parent=None):
        return cls(
            parent=parent,
            name=enum_dict["name"],
            description=enum_dict.get("description", ""),
            value=enum_dict["value"],
            is_default=None,
        )
