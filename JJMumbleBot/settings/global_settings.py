###############################################################################
# PLEASE NOTE THAT THE SETTINGS IN THIS FILE ARE FOR INTERNAL USE ONLY.
# END USERS MUST NOT CHANGE ANY SETTINGS HERE OR THE SOFTWARE MAY NOT FUNCTION PROPERLY.
###############################################################################

from JJMumbleBot.lib.enums import BotState

# Internal Settings
version: str = "v3.0.0"
bot_service = None
gui_service = None
log_service = None
# Monitor Service
monitor_service = None
monitor_thr = None
# Web Service
socket_service = None
# Config Instance
cfg = None
# Mumble Instance
mumble_inst = None
# Command Line Arguments
safe_mode: bool = False
debug_mode: bool = False
quiet_mode: bool = False
verbose_mode: bool = False
# Audio Thread Instance
audio_inst = None
audio_dni = (False, None)
# Bot State
status = BotState.OFFLINE
exit_flag: bool = False
# Command History
cmd_history = None
# Command Queue
cmd_queue = None
# Aliases
aliases = {}
# Initialized plugins.
bot_plugins = None


