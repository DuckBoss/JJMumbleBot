###############################################################################
# PLEASE NOTE THAT THE SETTINGS IN THIS FILE ARE FOR INTERNAL USE ONLY.
# END USERS MUST NOT CHANGE ANY SETTINGS HERE OR THE SOFTWARE MAY NOT FUNCTION PROPERLY.
###############################################################################


# INTERNAL SETTINGS
# Logging
use_logging: bool = False
max_logs: int = 15

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


# AUDIO SETTINGS
can_duck: bool = False
is_ducking: bool = False
duck_start: float = 0.0
duck_end: float = 0.0
ducking_volume: float = 0.05
ducking_threshold: float = 0.5
ducking_delay: float = 1
last_volume: float = 0.3
volume: float = 0.3

# DIRECTORY SETTINGS
# User Privileges Path
user_priv_path: str = ""
