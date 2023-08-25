from typing import Any, List, Optional

from pydantic.dataclasses import dataclass

from svd import basic_elements
from svd.basic_elements import Access, AddressBlockUsage
from svd.register import Register


@dataclass
class Peripheral:
    name: str
    base_address: int
    address_block: "AddressBlock"

    version: Optional[str] = None
    description: Optional[str] = None
    alternate_peripheral: Optional["Peripheral"] = None
    group_name: Optional[str] = None
    prepend_to_name: Optional[str] = None
    append_to_name: Optional[str] = None
    header_struct_name: Optional[str] = None
    disable_condition: Optional[str] = None
    size: Optional[int] = None
    access: Optional[Access] = None
    protection: Optional[str] = None
    reset_value: Optional[int] = None
    reset_mask: Optional[int] = None
    interrupt: Optional["Interrupt"] = None
    registers: Optional[List[Register]] = None

    derived_from: Optional["Peripheral"] = None
    parent: Optional[Any] = None

    @classmethod
    def from_dict(cls, peripheral_dict, parent=None):
        new_cls = cls(
            name=peripheral_dict.get("name"),
            base_address=basic_elements.parse_int(
                peripheral_dict.get("baseAddress")
            ),
            address_block=AddressBlock.from_dict(
                peripheral_dict.get("addressBlock")
            ),
            version=peripheral_dict.get("version"),
            description=peripheral_dict.get("description"),
            alternate_peripheral=peripheral_dict.get("alternate_peripheral"),
            group_name=peripheral_dict.get("group_name"),
            prepend_to_name=peripheral_dict.get("prepend_to_name"),
            append_to_name=peripheral_dict.get("append_to_name"),
            header_struct_name=peripheral_dict.get("header_struct_name"),
            disable_condition=peripheral_dict.get("disable_condition"),
            size=peripheral_dict.get("size"),
            access=peripheral_dict.get("access"),
            protection=peripheral_dict.get("protection"),
            reset_value=peripheral_dict.get("reset_value"),
            reset_mask=peripheral_dict.get("reset_mask"),
            interrupt=peripheral_dict.get("interrupt"),
            derived_from=peripheral_dict.get("derived_from"),
            parent=parent,
        )
        new_cls.parent = parent
        if registers := peripheral_dict.get("registers"):
            registers = registers["register"]
            registers = [Register.from_dict(r, new_cls) for r in registers]
        new_cls.registers = registers
        return new_cls


@dataclass
class AddressBlock:
    offset: int
    size: int
    usage: AddressBlockUsage
    protection: Optional[str] = None

    @classmethod
    def from_dict(cls, address_block_dict):
        return cls(
            offset=basic_elements.parse_int(address_block_dict.get("offset")),
            size=basic_elements.parse_int(address_block_dict.get("size")),
            usage=address_block_dict.get("usage"),
            protection=address_block_dict.get("protection"),
        )


@dataclass
class Interrupt:
    name: str
    value: int
    description: Optional[str] = None
