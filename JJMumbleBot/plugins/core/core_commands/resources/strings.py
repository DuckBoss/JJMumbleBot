from JJMumbleBot.lib.utils.runtime_utils import get_command_token

###########################################################################
# CORE COMMANDS PLUGIN CONFIG PARAMETER STRINGS

# ERROR STRINGS
CMD_INVALID_STOP_PLUGIN = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}stopplugin 'plugin_name'"
]
CMD_INVALID_START_PLUGIN = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}startplugin 'plugin_name'"
]
CMD_INVALID_RESTART_PLUGIN = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}restartplugin 'plugin_name'"
]
CMD_INVALID_SET_COMMENT = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}setcomment 'message'"
]
CMD_INVALID_REMOVE_ALIAS = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}removealias 'alias_name'"
]
CMD_INVALID_SET_ALIAS = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}setalias 'alias_name' (cmd) param | (cmd) param | ..."
]
CMD_INVALID_GET_CMD_PERMISSION = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}getpermission 'cmd_name'"
]
CMD_INVALID_SET_CMD_PERMISSION = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}changepermission 'cmd_name' 'permission_level'"
]
CMD_INVALID_SET_CMD_PERMISSION_RANGE = [
    "ERROR: Invalid command permission value!",
    "The permission value must be a valid permission level."
]
CMD_INVALID_IMPORT_PERMISSIONS = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}importpermissions 'url'"
]
CMD_INVALID_IMPORT_PRIVILEGES = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}importuserprivileges 'url'"
]
CMD_INVALID_IMPORT_ALIASES = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}importaliases 'url'"
]
