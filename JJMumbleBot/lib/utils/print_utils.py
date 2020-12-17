import JJMumbleBot.settings.global_settings as GS
from JJMumbleBot.lib.resources.strings import *
from enum import Enum


class PrintMode(Enum):
    NO_PRINT = -1,
    REG_PRINT = 0,
    VERBOSE_PRINT = 1


def dprint(msg, origin=None, error_type=None):
    if GS.verbose_mode and not GS.quiet_mode:
        print(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:'
              f'{"<"+error_type+">:" if error_type is not None else ""}{msg}')


def rprint(msg, origin=None, error_type=None):
    if not GS.quiet_mode:
        print(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:'
              f'{"<"+error_type+">:" if error_type is not None else ""}{msg}')
