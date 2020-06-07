import JJMumbleBot.settings.global_settings as global_settings
import JJMumbleBot.installer.quick_start as quick_start
from JJMumbleBot.lib.errors import ExitCodes
from JJMumbleBot.lib.resources.strings import DEBUG, CRITICAL
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.utils import rprint
from JJMumbleBot.lib.resources.strings import L_STARTUP
import sys


class CLAType:
    @staticmethod
    def cla_setup():
        quick_start.start()

    @staticmethod
    def cla_debug():
        import JJMumbleBot.lib.utils.utils as utils
        utils.debug_config()


def classify():
    if len(sys.argv) <= 1:
        return

    if "/setup" in sys.argv:
        CLAType.cla_setup()
        return
    if '-quiet' in sys.argv:
        global_settings.quiet_mode = True
        log(DEBUG, "Quiet mode has been enabled through system arguments.", origin=L_STARTUP)
    for arg in sys.argv[1:]:
        if arg == "-debug":
            global_settings.debug_mode = True
            rprint("Debug mode has been enabled.")
            log(DEBUG, "Debug mode has been enabled through system arguments.", origin=L_STARTUP)
        elif arg == "-safe":
            global_settings.safe_mode = True
            rprint("Safe mode has been enabled.")
            log(DEBUG, "Safe mode has been enabled through system arguments.", origin=L_STARTUP)
        elif arg == "-verbose":
            global_settings.verbose_mode = True
            rprint("Verbose mode has been enabled.")
            log(DEBUG, "Verbose mode has been enabled through system arguments.", origin=L_STARTUP)

    if global_settings.verbose_mode and global_settings.quiet_mode:
        from JJMumbleBot.lib.errors import SysArgError
        log(CRITICAL, "It looks like both verbose mode and quiet mode are enabled. "
                      "Only one or the other can be used!\n"
                      f"Error Code: {ExitCodes.SYS_ARG_ERROR.value}", origin=L_STARTUP)
        raise SysArgError("It looks like both verbose mode and quiet mode are enabled. "
                          "Only one or the other can be used!\n"
                          f"Error Code: {ExitCodes.SYS_ARG_ERROR.value}")
    if global_settings.debug_mode:
        CLAType.cla_debug()
