from typing import Any, Dict, List, Optional, Union

from pydantic.dataclasses import dataclass

from svd import basic_elements
from svd.basic_elements import Access, ModifiedWriteValues, ReadAction
from svd.field import Field


@dataclass
class Register:
    name: str
    address_offset: int
    display_name: Optional[str] = None
    description: Optional[str] = None
    alternate_group: Optional[str] = None
    alternate_register: Optional[Union[str, "Register"]] = None

    size: Optional[int] = None
    access: Optional[Access] = None
    protection: Optional[str] = None
    reset_value: Optional[int] = None
    reset_mask: Optional[int] = None

    data_type: Optional[str] = None
    modified_write_values: Optional[ModifiedWriteValues] = None
    write_constraint: Optional[Dict] = None
    read_action: Optional[ReadAction] = None
    fields: Optional[List[Field]] = None

    derived_from: Optional["Register"] = None
    parent: Optional[Any] = None

    @classmethod
    def from_dict(cls, register_dict, parent=None):
        new_cls = cls(
            name=register_dict.get("name"),
            address_offset=basic_elements.parse_int(
                register_dict.get("addressOffset")
            ),
            display_name=register_dict.get("displayName"),
            description=register_dict.get("description"),
            alternate_group=register_dict.get("alternateGroup"),
            alternate_register=register_dict.get("alternateRegister"),
            size=basic_elements.parse_int(
                register_dict.get("size", parent.size if parent else None)
            ),
            access=register_dict.get(
                "access", parent.access if parent else None
            ),
            protection=register_dict.get(
                "protection", parent.protection if parent else None
            ),
            reset_value=basic_elements.parse_int(
                register_dict.get(
                    "resetValue", parent.reset_value if parent else None
                )
            ),
            reset_mask=basic_elements.parse_int(
                register_dict.get(
                    "resetMask", parent.reset_mask if parent else None
                )
            ),
            data_type=register_dict.get("data_type"),
            modified_write_values=register_dict.get("modifiedWriteValues"),
            write_constraint=register_dict.get("writeConstraint"),
            read_action=register_dict.get("readAction"),
            derived_from=register_dict.get("derivedFrom"),
            parent=parent,
        )
        if fields := register_dict.get("fields"):
            fields = fields["field"]
            if isinstance(fields, list):
                fields = [Field.from_dict(f, new_cls) for f in fields]
            else:
                fields = [Field.from_dict(fields, new_cls)]
        new_cls.fields = fields
        return new_cls
