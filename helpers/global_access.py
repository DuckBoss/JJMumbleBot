import configparser
import time
import datetime
from pymumble.pymumble_py3.messages import Cmd as PyMessages
from pymumble.pymumble_py3.constants import *


class GlobalMods:
    # JJMumbleBot Data
    version = "v2.3.0"
    jjmumblebot = None
    # Whisper Target
    whisper_target = None
    # Audio Instance
    audio_thread = None
    audio_lock = False
    # Mumble Instance
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
    # Command history.
    cmd_history = None
    # Up-time Tracker
    start_seconds = None
    seconds = 0
    minutes = 0
    hours = 0
    days = 0


class RemoteTextMessage(PyMessages):
    def __init__(self, session, channel_id, message, actor):
        PyMessages.__init__(self)

        self.cmd = PYMUMBLE_CMD_TEXTMESSAGE
        self.actor = actor
        self.parameters = {"session": session,
                           "channel_id": channel_id,
                           "message": message,
                           "actor": actor}


def debug_print(msg):
    if GlobalMods.verbose_mode and not GlobalMods.quiet_mode:
        print(msg)


def reg_print(msg):
    if not GlobalMods.quiet_mode:
        print(msg)


def check_time():
    GlobalMods.seconds = time.time() - GlobalMods.start_seconds
    return f"Up-time: {str(datetime.timedelta(seconds=GlobalMods.seconds)).split('.')[0]}"
