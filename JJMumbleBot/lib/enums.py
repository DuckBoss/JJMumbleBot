import enum


class BotState(enum.Enum):
    OFFLINE = 0,
    ONLINE = 1,
    PROCESSING = 2,
    ERROR = 3

