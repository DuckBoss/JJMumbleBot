from JJMumbleBot.lib.utils.runtime_utils import get_command_token

###########################################################################
# AUDIO COMMANDS PLUGIN CONFIG PARAMETER STRINGS

# ERROR STRINGS
CMD_INVALID_SEEK_VALUE = "Invalid seek input provided!"
CMD_INVALID_SEEK = ["ERROR: Incorrect command formatting!",
                    f"Available Formats:",
                    f"{get_command_token()}seek 'hrs:mins:secs'",
                    f"{get_command_token()}seek 'mins:secs'",
                    f"{get_command_token()}seek 'seconds'"]
CMD_INVALID_REMOVE = ["ERROR: Incorrect command formatting!",
                      f"Format: {get_command_token()}remove 'track_number'"]

CMD_INVALID_VOLUME = "Invalid Volume input provided! The volume must be between 0 and 1"
CMD_INVALID_DUCKING_THRESHOLD = "Invalid Ducking threshold input provided! [Recommended: 3000-4000]"
CMD_INVALID_DUCKING_DELAY = "Invalid Ducking delay input provided! [Recommended: 0-5]"
