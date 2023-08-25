import logging
import re
from enum import Enum
from typing import Optional, Union

_logger = logging.getLogger(__name__)


class Access(Enum):
    READ_ONLY = "read-only"
    WRITE_ONLY = "write-only"
    READ_WRITE = "read-write"
    WRITE_ONCE = "writeOnce"
    READ_WRITE_ONCE = "read-writeOnce"


class AddressBlockUsage(Enum):
    REGISTERS = "registers"
    BUFFER = "buffer"
    RESERVED = "reserved"


class Endian(Enum):
    LITTLE = "little"
    BIG = "big"
    SELECTABLE = "selectable"
    OTHER = "other"


class ModifiedWriteValues(Enum):
    ONE_TO_CLEAR = "oneToClear"
    ONE_TO_SET = "oneToSet"
    ONE_TO_TOGGLE = "oneToToggle"
    ZERO_TO_CLEAR = "zeroToClear"
    ZERO_TO_SET = "zeroToSet"
    ZERO_TO_TOGGLE = "zeroToToggle"
    CLEAR = "clear"
    SET = "set"
    MODIFY = "modify"


class ReadAction(Enum):
    CLEAR = "clear"
    SET = "set"
    MODIFY = "modify"
    MODIFY_EXTERNAL = "modify_external"


class Usage(Enum):
    READ = "read"
    WRITE = "write"
    READ_WRITE = "read-write"

    def c_modifier(self):
        match self:
            case Usage.READ:
                return "const"
            case Usage.WRITE:
                return ""
            case Usage.READ_WRITE:
                return ""


def parse_int(value: Optional[Union[int, str]]):
    if value is None:
        return value
    if not isinstance(value, str):
        return value
    value: str = value

    value = value.strip()

    hex_str = re.match(r"0[xX]([0-9a-fA-F]+)\b", value)
    if hex_str:
        value = hex_str.groups()[0]
        value = int(value, 16)
        return value

    bin_str = re.match(r"0b([0-1x]+)\b", value) or re.match(
        r"#([0-1x]+)\b", value
    )
    if bin_str:
        value = bin_str.groups()[0]
        value = value.replace("x", "0")
        value = int(value, 2)
        return value

    return int(value)


def parse_description(value: Optional[str]):
    if value is None:
        return value
    return re.sub(r"[\s\n\r]+", " ", value)
