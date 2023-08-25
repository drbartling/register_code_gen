import logging
from typing import Any, List, Optional, Union

from pydantic.dataclasses import dataclass

from svd import basic_elements
from svd.basic_elements import Access, AddressBlockUsage
from svd.register import Register

_logger = logging.getLogger(__name__)


@dataclass
class Peripheral:
    name: str
    base_address: int
    address_block: Optional["AddressBlock"] = None

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

    interrupt: Optional[List["Interrupt"]] = None
    registers: Optional[List[Register]] = None

    derived_from: Optional[Union[str, "Peripheral"]] = None
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
            description=basic_elements.parse_description(
                peripheral_dict.get("description")
            ),
            alternate_peripheral=peripheral_dict.get("alternatePeripheral"),
            group_name=peripheral_dict.get("group_name"),
            prepend_to_name=peripheral_dict.get("prependToName"),
            append_to_name=peripheral_dict.get("append_to_name"),
            header_struct_name=peripheral_dict.get("headerStructName"),
            disable_condition=peripheral_dict.get("disableCondition"),
            size=basic_elements.parse_int(
                peripheral_dict.get("size", parent.size if parent else None)
            ),
            access=peripheral_dict.get(
                "access", parent.access if parent else None
            ),
            protection=peripheral_dict.get(
                "protection", parent.protection if parent else None
            ),
            reset_value=basic_elements.parse_int(
                peripheral_dict.get(
                    "reset_value", parent.reset_value if parent else None
                )
            ),
            reset_mask=basic_elements.parse_int(
                peripheral_dict.get(
                    "reset_mask", parent.reset_mask if parent else None
                )
            ),
            derived_from=peripheral_dict.get("@derivedFrom"),
            parent=parent,
        )

        if interrupt := peripheral_dict.get("interrupt"):
            interrupt = Interrupt.from_dict(interrupt, new_cls)
        new_cls.interrupt = interrupt

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
        if None is address_block_dict:
            return None

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
    parent: Optional[Union[Peripheral, str]] = None

    @classmethod
    def from_dict(cls, interrupt_dict, parent=None):
        if isinstance(interrupt_dict, dict):
            interrupt_dict = [interrupt_dict]
        return [
            cls(
                name=i.get("name"),
                value=i.get("value"),
                description=i.get("description"),
                parent=parent,
            )
            for i in interrupt_dict
        ]
