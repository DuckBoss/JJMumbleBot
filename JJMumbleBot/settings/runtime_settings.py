###############################################################################
# PLEASE NOTE THAT THE SETTINGS IN THIS FILE ARE FOR INTERNAL USE ONLY.
# END USERS MUST NOT CHANGE ANY SETTINGS HERE OR THE SOFTWARE MAY NOT FUNCTION PROPERLY.
###############################################################################


# INTERNAL SETTINGS
# Logging
use_logging: bool = False
max_logs: int = 15
max_log_size: int = 150000

# COMMAND SETTINGS
# Command Tick Rate
tick_rate: float = 0.1
# Multi-Command Limit
multi_cmd_limit: int = 10
# Command Token
cmd_token: str = '!'
# Command History Limit
cmd_hist_lim: int = 25
# Command Queue Limit
cmd_queue_lim: int = 50

# Whisper Target
whisper_target = None
# Global Mute Access
muted = False
# Up-Time Tracking
start_time = 0

# DIRECTORY SETTINGS
# User Privileges Path
user_priv_path: str = ""
