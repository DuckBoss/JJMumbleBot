from JJMumbleBot.lib.utils.runtime_utils import get_command_token

###########################################################################
# SOUND BOARD PLUGIN CONFIG PARAMETER STRINGS
P_PLAY_AUDIO_CLIP_ON_USER_JOIN = 'PlayAudioClipOnUserJoin'
P_PLAY_CLIP_ONLY_IF_USERS_IN_CHANNEL = 'PlayAudioClipOnlyIfUsersInChannel'
P_PLAY_SAME_CLIP_ON_USER_JOIN = 'PlaySameAudioClipOnAllUserJoin'
P_GENERIC_CLIP_TO_PLAY_ON_USER_JOIN = 'GenericAudioClipOnUserJoin'

# COMMAND ERROR STRINGS
CMD_INVALID_CLEAR_USER_CONNECTION = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}clearuserconnectionsound 'username'"
]
CMD_INVALID_SET_USER_DEFAULT_CONNECTION = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}setdefaultconnectionsound 'audio_clip_name'"
]
CMD_INVALID_SET_USER_CONNECTION = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}setuserconnectionsound 'username' 'audio_clip_name'"
]
CMD_INVALID_GET_USER_CONNECTION = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}getuserconnectionsound 'username'"
]


