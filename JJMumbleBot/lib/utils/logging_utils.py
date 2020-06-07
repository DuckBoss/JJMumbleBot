from JJMumbleBot.settings import global_settings
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.lib.resources.strings import INFO, DEBUG, WARNING, CRITICAL, META_NAME, META_VERSION, L_GENERAL, C_LOGGING, P_LOG_DIR
import logging


def initialize_logging():
    if not runtime_settings.use_logging:
        return
    from logging.handlers import TimedRotatingFileHandler
    logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
    log_file_name = f"{global_settings.cfg[C_LOGGING][P_LOG_DIR]}/runtime.log"
    global_settings.log_service = logging.getLogger("RuntimeLogging")
    global_settings.log_service.setLevel(logging.DEBUG)

    handler = TimedRotatingFileHandler(log_file_name, when='midnight', backupCount=runtime_settings.max_logs)
    handler.setLevel(logging.INFO)
    log_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    handler.setFormatter(log_formatter)
    global_settings.log_service.addHandler(handler)


def log(level, message, origin=None):
    if not runtime_settings.use_logging:
        return
    if not global_settings.log_service:
        return
    if level == INFO:
        global_settings.log_service.info(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:{message}')
    elif level == DEBUG:
        global_settings.log_service.debug(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:{message}')
    elif level == WARNING:
        global_settings.log_service.warning(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:{message}')
    elif level == CRITICAL:
        global_settings.log_service.critical(f'[{META_NAME}({META_VERSION}).{origin if origin is not None else L_GENERAL}]:{message}')
