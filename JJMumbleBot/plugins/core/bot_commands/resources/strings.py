from JJMumbleBot.lib.utils.runtime_utils import get_command_token

###########################################################################
# BOT COMMANDS PLUGIN CONFIG PARAMETER STRINGS

# INFO STRINGS
INFO_DISPLAYED_PLUGINS = "Displayed all active plugins."
INFO_DISPLAYED_CMD_SEARCH = "Displayed command search results."
INFO_LEFT_CHANNEL = "Returned to default channel."
INFO_REMOVE_CHANNEL = "Removed current channel."
INFO_DISPLAYED_BLACKLIST = "Displayed all blacklisted user."

# ERROR STRINGS
ERR_DATABASE_CMD = "There was an error retrieving the commands from the database."
ERR_DATABASE_ALIAS = "There was an error retrieving the aliases from the database."

# COMMAND ERROR STRINGS
CMD_INVALID_ECHO = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}echo 'message'"
]
CMD_INVALID_MSG = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}msg 'username' 'message'"
]
CMD_INVALID_LOG = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}log 'message'"
]
CMD_INVALID_MOVE = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}move 'channel_name'"
]
CMD_INVALID_MAKE = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}makechannel 'channel_name'"
]
CMD_INVALID_JOIN_USER = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}joinuser 'username'"
]
CMD_INVALID_ALIAS_SEARCH = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}aliassearch 'alias'"
]
CMD_INVALID_CMD_SEARCH = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}cmdsearch 'command'"
]
CMD_INVALID_SET_PRIVILEGES = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}setprivileges 'username' 'level'"
]
CMD_INVALID_ADD_PRIVILEGES = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}addprivileges 'username' 'level'"
]
CMD_INVALID_BLACKLIST_USER = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}blacklistuser 'username'"
]
CMD_INVALID_WHITELIST_USER = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}whitelistuser 'username'"
]