from JJMumbleBot.lib.utils.runtime_utils import get_command_token

###########################################################################
# BOT COMMANDS PLUGIN CONFIG PARAMETER STRINGS

# INFO STRINGS
INFO_DISPLAYED_PLUGINS = "Displayed all active plugins."
INFO_DISPLAYED_CMD_SEARCH = "Displayed command search results."
INFO_LEFT_CHANNEL = "Returned to default channel."
INFO_REMOVE_CHANNEL = "Removed a channel."
INFO_DISPLAYED_BLACKLIST = "Displayed all blacklisted user."

# ERROR STRINGS
ERR_DATABASE_CMD = "There was an error retrieving the commands from the database."
ERR_DATABASE_ALIAS = "There was an error retrieving the aliases from the database."
ERR_STD = "ERROR: Incorrect command formatting!"

# COMMAND ERROR STRINGS
CMD_INVALID_ECHO = [
    ERR_STD,
    f"Format: {get_command_token()}echo 'message'"
]
CMD_INVALID_MSG = [
    ERR_STD,
    f"Format: {get_command_token()}msg 'username' 'message'"
]
CMD_INVALID_RENAME_CHANNEL = [
    ERR_STD,
    f"Format: {get_command_token()}renamechannel 'channel_name' 'new_channel_name'"
]
CMD_INVALID_MOVE_USER = [
    ERR_STD,
    f"Format: {get_command_token()}moveuser 'username' 'channel_name'"
]
CMD_INVALID_KICK = [
    ERR_STD,
    f"Format: {get_command_token()}kick 'username' 'reason'"
]
CMD_INVALID_BAN = [
    ERR_STD,
    f"Format: {get_command_token()}ban 'username' 'reason'"
]
CMD_INVALID_LOG = [
    ERR_STD,
    f"Format: {get_command_token()}log 'message'"
]
CMD_INVALID_MOVE = [
    ERR_STD,
    f"Format: {get_command_token()}move 'channel_name'"
]
CMD_INVALID_MAKE_TEMP = [
    ERR_STD,
    f"Format: {get_command_token()}makechannel 'channel_name'"
]
CMD_INVALID_MAKE_PERM = [
    ERR_STD,
    f"Format: {get_command_token()}makepermanentchannel 'channel_name'"
]
CMD_INVALID_REMOVE = [
    ERR_STD,
    f"Format: {get_command_token()}removechannel 'channel_name'"
]
CMD_INVALID_JOIN_USER = [
    ERR_STD,
    f"Format: {get_command_token()}joinuser 'username'"
]
CMD_INVALID_MUTE_USER = [
    ERR_STD,
    f"Format: {get_command_token()}muteuser 'username'"
]
CMD_INVALID_UNMUTE_USER = [
    ERR_STD,
    f"Format: {get_command_token()}unmuteuser 'username'"
]
CMD_INVALID_DEAFEN_USER = [
    ERR_STD,
    f"Format: {get_command_token()}deafenuser 'username'"
]
CMD_INVALID_UNDEAFEN_USER = [
    ERR_STD,
    f"Format: {get_command_token()}undeafenuser 'username'"
]
CMD_INVALID_ALIAS_SEARCH = [
    ERR_STD,
    f"Format: {get_command_token()}aliassearch 'alias'"
]
CMD_INVALID_CMD_SEARCH = [
    ERR_STD,
    f"Format: {get_command_token()}cmdsearch 'command'"
]
CMD_INVALID_SET_PRIVILEGES = [
    ERR_STD,
    f"Format: {get_command_token()}setprivileges 'username' 'level'"
]
CMD_INVALID_ADD_PRIVILEGES = [
    ERR_STD,
    f"Format: {get_command_token()}addprivileges 'username' 'level'"
]
CMD_INVALID_BLACKLIST_USER = [
    ERR_STD,
    f"Format: {get_command_token()}blacklistuser 'username'"
]
CMD_INVALID_WHITELIST_USER = [
    ERR_STD,
    f"Format: {get_command_token()}whitelistuser 'username'"
]