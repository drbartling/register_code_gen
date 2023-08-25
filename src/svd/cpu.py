from typing import Any, Optional

from pydantic.dataclasses import dataclass

from svd import basic_elements
from svd.basic_elements import Endian


@dataclass
class Cpu:
    name: str
    revision: str
    endian: Endian
    mpu_present: bool
    fpu_present: bool
    nvic_prio_bits: int
    vendor_systick_config: bool
    parent: Optional[Any] = None

    @classmethod
    def from_dict(cls, cpu_dict, parent=None):
        return cls(
            name=cpu_dict.get("name"),
            revision=cpu_dict.get("revision"),
            endian=cpu_dict.get("endian"),
            mpu_present=cpu_dict.get("mpuPresent"),
            fpu_present=cpu_dict.get("fpuPresent"),
            nvic_prio_bits=basic_elements.parse_int(
                cpu_dict.get("nvicPrioBits")
            ),
            vendor_systick_config=cpu_dict.get("vendorSystickConfig"),
            parent=parent,
        )
