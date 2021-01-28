from JJMumbleBot.lib.utils.runtime_utils import get_command_token

###########################################################################
# WHISPER PLUGIN CONFIG PARAMETER STRINGS

# INFO STRINGS
INFO_ADDED_MULTIPLE_WHISPER = "Added whisper to multiple users!"
INFO_INVALID_WHISPER_CLIENT = "Can't set the whisper target to the bot."

# COMMAND ERROR STRINGS
CMD_INVALID_SET_WHISPER = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}setwhisperuser 'username'"
]
CMD_INVALID_SET_WHISPER_USERS = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}setwhisperusers username0 username1 ..."
]
CMD_INVALID_REMOVE_WHISPER = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}removewhisperuser 'username'"
]
CMD_INVALID_ADD_WHISPER = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}addwhisperuser 'username'"
]
CMD_INVALID_WHISPER_CHANNEL = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}setwhisperchannel 'channel_name'"
]