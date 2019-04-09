import configparser


class GlobalMods:
    cfg = configparser.ConfigParser()
    logger = None
    muted = True
    debug_mode = False
    safe_mode = False
    verbose_mode = False
    quiet_mode = False


def debug_print(msg):
    if GlobalMods.verbose_mode and not GlobalMods.quiet_mode:
        print(msg)


def reg_print(msg):
    if not GlobalMods.quiet_mode:
        print(msg)
