import functools
from typing import List, Optional

from pydantic.dataclasses import dataclass

from svd import basic_elements
from svd.basic_elements import Access
from svd.cpu import Cpu
from svd.peripheral import Peripheral


@dataclass
class Device:
    name: str
    version: str
    description: str
    address_unit_bites: int
    width: int

    vendor: Optional[str] = None
    vendor_id: Optional[str] = None
    series: Optional[str] = None
    license_text: Optional[str] = None
    cpu: Optional[Cpu] = None
    header_system_filename: Optional[str] = None
    gheader_definitions_prefix: Optional[str] = None

    size: Optional[int] = None
    access: Optional[Access] = None
    protection: Optional[str] = None
    reset_value: Optional[int] = None
    reset_mask: Optional[int] = None

    peripherals: Optional[List[Peripheral]] = None

    @classmethod
    def from_dict(cls, device_dict):
        new_cls = cls(
            vendor=device_dict.get("vendor"),
            vendor_id=device_dict.get("vendorID"),
            name=device_dict.get("name"),
            series=device_dict.get("series"),
            version=device_dict.get("version"),
            description=device_dict.get("description"),
            license_text=device_dict.get("licenseText"),
            cpu=Cpu.from_dict(device_dict.get("cpu")),
            header_system_filename=device_dict.get("headerSystemFilename"),
            gheader_definitions_prefix=device_dict.get(
                "headerDefinitionsPrefix"
            ),
            address_unit_bites=basic_elements.parse_int(
                device_dict.get("addressUnitBits")
            ),
            width=basic_elements.parse_int(device_dict.get("width")),
            size=basic_elements.parse_int(device_dict.get("size")),
            access=device_dict.get("access"),
            protection=device_dict.get("protection"),
            reset_value=basic_elements.parse_int(device_dict.get("resetValue")),
            reset_mask=basic_elements.parse_int(device_dict.get("resetMask")),
        )
        peripherals = device_dict["peripherals"]["peripheral"]
        peripherals = [Peripheral.from_dict(p, new_cls) for p in peripherals]
        new_cls.peripherals = peripherals

        for peripheral in new_cls.peripherals:
            if isinstance(peripheral.derived_from, str):

                def is_match(p: Peripheral, derived_name: str):
                    return p.name == derived_name

                is_match = functools.partial(
                    is_match, derived_name=peripheral.derived_from
                )

                peripheral.derived_from = list(
                    filter(is_match, new_cls.peripherals)
                )[0]
        return new_cls
