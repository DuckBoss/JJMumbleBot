import configparser


class GlobalMods:
    # Config Access
    cfg = configparser.ConfigParser()
    # PGUI System Access
    gui = None
    # Logger Access
    logger = None
    # Global Mute Access
    muted = True
    # System Arguments Access
    debug_mode = False
    safe_mode = False
    verbose_mode = False
    quiet_mode = False
    # Main Class Access
    jjmumblebot = None


def debug_print(msg):
    if GlobalMods.verbose_mode and not GlobalMods.quiet_mode:
        print(msg)


def reg_print(msg):
    if not GlobalMods.quiet_mode:
        print(msg)
