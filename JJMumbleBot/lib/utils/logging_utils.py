from typing import List, Union
from JJMumbleBot.settings import global_settings
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.lib.resources.strings import INFO, DEBUG, WARNING, ERROR, CRITICAL, META_NAME, META_VERSION, L_GENERAL, C_LOGGING, P_LOG_DIR
from JJMumbleBot.lib.utils.print_utils import rprint, dprint, PrintMode
import logging
import traceback


def initialize_logging():
    if not runtime_settings.use_logging:
        return
    from logging.handlers import RotatingFileHandler
    logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
    log_file_name = f"{global_settings.cfg[C_LOGGING][P_LOG_DIR]}/runtime.log"
    global_settings.log_service = logging.getLogger("RuntimeLogging")
    global_settings.log_service.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(log_file_name, maxBytes=int(runtime_settings.max_log_size), backupCount=int(runtime_settings.max_logs))
    handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter('[%(asctime)s]-[%(levelname)s]-%(message)s')
    handler.setFormatter(log_formatter)
    global_settings.log_service.addHandler(handler)


def log(level: str, message: Union[List[str], str], origin: str = None, error_type: str = None, gui_service=None, print_mode: int = -1):
    # Don't attempt to log anything if the use_logging flag is false.
    if not runtime_settings.use_logging:
        return
    # If logging is enabled and the log service is missing, raise an error.
    if global_settings.log_service is None:
        from JJMumbleBot.lib.errors import LogError
        raise LogError("ERROR: Logging is enabled but an instance of the logging service could not be created!")
    # If the provided message is not a list, convert it to a list.
    if not isinstance(message, list):
        message = [message]
    # Format the log messages for outputting.
    log_msg = "\n".join(message) if len(message) > 1 else message[0]
    log_out = f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]: ' \
              f'{"<"+error_type+">:" if error_type is not None else ""}{log_msg}'
    # If log stack tracing is enabled, include the stack trace in the log message.
    if runtime_settings.log_trace:
        log_out += f"\n{''.join(traceback.format_stack())}\n"
    # Log the formatted message based on the logging level.
    if level == INFO:
        global_settings.log_service.info(log_out)
    elif level == DEBUG:
        global_settings.log_service.debug(log_out)
    elif level == WARNING:
        global_settings.log_service.warning(log_out)
    elif level == ERROR:
        global_settings.log_service.error(log_out)
    elif level == CRITICAL:
        global_settings.log_service.critical(log_out)
    # Additionally, print out the log message if required.
    if print_mode == PrintMode.REG_PRINT.value:
        rprint(log_msg, origin=origin, error_type=error_type)
    elif print_mode == PrintMode.VERBOSE_PRINT.value:
        dprint(log_msg, origin=origin, error_type=error_type)
