###############################################################################
# PLEASE NOTE THAT THE SETTINGS IN THIS FILE ARE FOR INTERNAL USE ONLY.
# END USERS MUST NOT CHANGE ANY SETTINGS HERE OR THE SOFTWARE MAY NOT FUNCTION PROPERLY.
###############################################################################

# Internal Settings
bot_service = None
gui_service = None
log_service = None
# Web Interface
flask_server = None
socket_server = None
# Config Instance
cfg = None
# Mumble Instance
mumble_inst = None
# Bot Database Instance String (In Memory)
mumble_db_string = None
# Command Line Arguments
safe_mode: bool = False
debug_mode: bool = False
quiet_mode: bool = False
verbose_mode: bool = False
# Audio Thread Instance
vlc_inst = None
vlc_thread = None
audio_dni = (False, None)
vlc_interface = None
vlc_status = None
# Bot State
exit_flag: bool = False
# Command History
cmd_history = None
# Command Queue
cmd_queue = None
# Aliases
aliases = {}
# Initialized Plugins.
bot_plugins = None
# Last Command Output
last_command_type = ''
last_command_output = ''
