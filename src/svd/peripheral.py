from typing import Any, List, Optional

from pydantic.dataclasses import dataclass

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


@dataclass
class AddressBlock:
    offset: int
    size: int
    usage: AddressBlockUsage
    protection: Optional[str] = None


@dataclass
class Interrupt:
    name: str
    value: int
    description: Optional[str] = None
