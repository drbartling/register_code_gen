from typing import Dict, Optional

from pydantic.dataclasses import dataclass

from svd.basic_elements import Access, ModifiedWriteValues, ReadAction
from svd.enum_value import EnumeratedValues


@dataclass
class Field:
    name: str
    bit_offset: int
    bit_width: int
    description: Optional[str] = None
    access: Optional[Access] = None
    modified_write_values: Optional[ModifiedWriteValues] = None
    write_constraint: Optional[Dict] = None
    read_action: Optional[ReadAction] = None
    enumerated_values: Optional[EnumeratedValues] = None
    derived_from: Optional["Field"] = None

    @classmethod
    def from_dict(cls, field_dict):
        new_cls = cls(
            name=field_dict["name"],
            bit_offset=field_dict.get("bitOffset"),
            bit_width=field_dict.get("bitWidth"),
            description=field_dict.get("description"),
            access=field_dict.get("access"),
            modified_write_values=field_dict.get("modified_write_values"),
            write_constraint=field_dict.get("write_constraint"),
            read_action=field_dict.get("readAction"),
        )

        if enum_values := field_dict.get("enumeratedValues"):
            enum_values = EnumeratedValues.from_dict(enum_values, new_cls)
        new_cls.enumerated_values = enum_values
        return new_cls
