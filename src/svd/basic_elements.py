from enum import Enum


class Access(Enum):
    READ_ONLY = "read-only"
    WRITE_ONLY = "write-only"
    READ_WRITE = "read-write"
    WRITE_ONCE = "writeOnce"
    READ_WRITE_ONCE = "read-writeOnce"


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
