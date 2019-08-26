import enum


class BotState(enum.Enum):
    OFFLINE = 0,
    ONLINE = 1,
    PROCESSING = 2,
    ERROR = 3


class ExitCodes(enum.Enum):
    NORMAL = 0,
    UNKNOWN_ERROR = 1,
    SETUP_ERROR = 2,
    SYS_ARG_ERROR = 3
