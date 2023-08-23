from enum import Enum


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
