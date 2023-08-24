from typing import Dict, Optional

from pydantic.dataclasses import dataclass

from svd.basic_elements import Access, ModifiedWriteValues, ReadAction
from svd.enum_value import EnumeratedValues


@dataclass
class Field:
    name: str
    description: Optional[str]
    bit_offset: int
    bit_width: int
    access: Optional[Access]
    modified_write_values: Optional[ModifiedWriteValues]
    write_constraint: Optional[Dict]
    read_action: Optional[ReadAction]
    enumerated_values: Optional[EnumeratedValues]
