import configparser
import time


class GlobalMods:
    # Mumble instance
    mumble = None
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
    # Up-time Tracker
    start_seconds = None
    seconds = 0
    minutes = 0
    hours = 0
    days = 0


def debug_print(msg):
    if GlobalMods.verbose_mode and not GlobalMods.quiet_mode:
        print(msg)


def reg_print(msg):
    if not GlobalMods.quiet_mode:
        print(msg)


def check_time():
    GlobalMods.seconds = time.time() - GlobalMods.start_seconds
    while GlobalMods.seconds >= 60:
        GlobalMods.minutes += 1
        GlobalMods.seconds -= 60
    while GlobalMods.minutes >= 60:
        GlobalMods.hours += 1
        GlobalMods.minutes -= 60
    while GlobalMods.hours >= 24:
        GlobalMods.days += 1
        GlobalMods.hours -= 24
    return "Up-time: {%dd : %dh : %dm : %ds}" % (int(GlobalMods.days), int(GlobalMods.hours), int(GlobalMods.minutes), int(GlobalMods.seconds))
