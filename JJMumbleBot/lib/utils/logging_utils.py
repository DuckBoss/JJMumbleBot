from JJMumbleBot.settings import global_settings
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.lib.resources.strings import INFO, DEBUG, WARNING, CRITICAL, META_NAME, META_VERSION, L_GENERAL, C_LOGGING, P_LOG_DIR
from JJMumbleBot.lib.utils.print_utils import rprint, dprint, PrintMode
import logging


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


def display_error(gui_service, message: str):
    gui_service.quick_gui(
        message,
        text_type='header',
        text_align='left',
        box_align='left'
    )


def log(level: str, message: str, origin: str = None, error_type: str = None, gui_service=None, print_mode: int = -1):
    # Don't attempt to log anything if the use_logging flag is false.
    if not runtime_settings.use_logging:
        return
    # If logging is enabled and the log service is missing, raise an error.
    if global_settings.log_service is None:
        from JJMumbleBot.lib.errors import LogError
        raise LogError("ERROR: Logging is enabled but an instance of the logging service could not be created!")
    # Log the message based on the event level.
    if level == INFO:
        global_settings.log_service.info(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:'
                                         f'{"<"+error_type+">:" if error_type is not None else ""}{message}')
    elif level == DEBUG:
        global_settings.log_service.debug(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:'
                                          f'{"<"+error_type+">:" if error_type is not None else ""}{message}')
    elif level == WARNING:
        global_settings.log_service.warning(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:'
                                            f'{"<"+error_type+">:" if error_type is not None else ""}{message}')
    elif level == CRITICAL:
        global_settings.log_service.critical(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:'
                                             f'{"<"+error_type+">:" if error_type is not None else ""}{message}')
    # Additionally, print out the log message if required.
    if print_mode == PrintMode.REG_PRINT.value:
        rprint(message, error_type=error_type)
    elif print_mode == PrintMode.DEBUG_PRINT.value:
        dprint(message, error_type=error_type)
    # Display the error in the mumble channel chat if required.
    if error_type is not None and gui_service is not None:
        display_error(gui_service, message)


