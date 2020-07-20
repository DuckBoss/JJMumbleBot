import JJMumbleBot.settings.global_settings as GS
from JJMumbleBot.lib.resources.strings import *


def dprint(msg, origin=None):
    if GS.verbose_mode and not GS.quiet_mode:
        print(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:{msg}')


def rprint(msg, origin=None):
    if not GS.quiet_mode:
        print(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:{msg}')
