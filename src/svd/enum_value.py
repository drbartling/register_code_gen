import re
from typing import List, Optional, Union

from pydantic.dataclasses import dataclass

from svd.usage import Usage


@dataclass
class Field:
    pass


@dataclass
class EnumeratedValues:
    parent: Optional["Field"]
    derived_from: Optional["EnumeratedValues"]
    name: str
    usage: Usage
    enumerated_values: List["EnumeratedValue"]


@dataclass
class EnumeratedValue:
    parent: Optional[EnumeratedValues]
    derived_from: Optional["EnumeratedValues"]
    name: str
    description: str
    value: Optional[Union[int, str]]
    is_default: Optional[bool]

    def __post_init__(self):
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

    @classmethod
    def from_dict(cls, enum_dict):
        return cls(
            None,
            None,
            enum_dict["name"],
            enum_dict.get("description", ""),
            enum_dict["value"],
            None,
        )
