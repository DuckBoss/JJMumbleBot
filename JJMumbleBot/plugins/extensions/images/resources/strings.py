from JJMumbleBot.lib.utils.runtime_utils import get_command_token

###########################################################################
# IMAGES PLUGIN CONFIG PARAMETER STRINGS
P_FRAME_COL = 'ImageFrameColor'
P_FRAME_SIZE = 'ImageFrameSize'

# INFO STRINGS
INFO_POSTED_IMAGE = "Posted an image to the mumble channel chat."
INFO_SEARCH_RESULTS = "Displayed image search results in the mumble channel chat."
INFO_DISPLAYED_ALL = "Displayed a list of all locally stored images."

# COMMAND ERROR STRINGS
CMD_INVALID_POST = f"ERROR: Incorrect command formatting!<br>Format: {get_command_token()}post 'url'"
CMD_INVALID_IMGSEARCH = f"ERROR: Incorrect command formatting!<br>Format: {get_command_token()}imgsearch 'file_name'"
CMD_IMAGE_DNE = "ERROR: The image does not exist. Please make sure the spelling matches the file name."

# GENERAL ERROR STRINGS
GEN_HTTP_ERROR = "ERROR: Encountered an HTTP Error while trying to retrieve the image."
GEN_INVALID_SCHEMA_ERROR = "ERROR: Encountered an Invalid Schema Error while trying to retrieve the image."
GEN_REQUESTS_ERROR = "ERROR: Encountered a Requests Module Error while trying to retrieve the image."
