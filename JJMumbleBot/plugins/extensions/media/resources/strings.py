from JJMumbleBot.lib.utils.runtime_utils import get_command_token

###########################################################################
# YOTUUBE CONFIG PARAMETER STRINGS
P_YT_MAX_SEARCH_LEN = 'MaxSearchLength'
P_YT_MAX_VID_LEN = 'MaxVideoLength'
P_YT_MAX_PLAY_LEN = 'MaxPlaylistLength'
P_YT_ALL_PLAY_MAX = 'AllowPlaylistMax'

# COMMAND ERROR STRINGS
CMD_INVALID_LINK = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}link 'url'"
]
CMD_INVALID_LINK_FRONT = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}linkfront 'url'"
]
CMD_INVALID_YTSEARCH = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}ytsearch 'url'"
]
CMD_INVALID_YTPLAY = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}ytplay 'track_number'"
]
