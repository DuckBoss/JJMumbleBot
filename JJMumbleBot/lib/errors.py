import enum


class ExitCodes(enum.Enum):
    NORMAL = 0
    UNKNOWN_ERROR = 1
    SETUP_ERROR = 2
    SYS_ARG_ERROR = 3
    PLUGIN_ERROR = 4
    SAFE_MODE_ERROR = 5
    CONFIG_ERROR = 6
    AUDIO_ERROR = 7


class UnknownError(Exception):
    pass


class SetupError(Exception):
    pass


class SysArgError(Exception):
    pass


class ConfigError(Exception):
    pass


class PluginError(Exception):
    pass


class SafeModeError(Exception):
    pass


class AudioError(Exception):
    pass