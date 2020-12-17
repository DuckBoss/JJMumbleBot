from JJMumbleBot.lib.utils.runtime_utils import get_command_token

###########################################################################
# AUTO-UPDATER PLUGIN CONFIG PARAMETER STRINGS
P_PIP_CMD = 'PIPCommand'

# COMMAND ERROR STRINGS
CMD_INVALID_UPDATE = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}updatedependency 'dependency_name'"
    ]
CMD_INVALID_CHECK = [
    "ERROR: Incorrect command formatting!",
    f"Format: {get_command_token()}checkforupdates 'dependency_name'"
    ]
