from JJMumbleBot.settings import global_settings
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.lib.mumble_data import MumbleData
from JJMumbleBot.lib.web.web_interface import web_service
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.resources.strings import *
import logging


class BotServiceHelper:
    @staticmethod
    def retrieve_mumble_data():
        server_ip: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_IP]
        server_pass: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_PASS]
        server_port: int = int(global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_PORT])
        user_id: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID]
        user_cert: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_CERT]
        return MumbleData(ip=server_ip, port=server_port, uid=user_id, pwd=server_pass, cert=user_cert)

    @staticmethod
    def initialize_settings():
        from JJMumbleBot.lib.utils import dir_utils
        import configparser
        global_settings.cfg = configparser.ConfigParser()
        global_settings.cfg.read(f"{dir_utils.get_main_dir()}/config.ini")

        runtime_settings.tick_rate = float(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TICK_RATE])
        runtime_settings.cmd_hist_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_MULTI_LIM])
        runtime_settings.cmd_token = global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]
        runtime_settings.use_logging = global_settings.cfg.getboolean(C_LOGGING, P_LOG_ENABLE, fallback=False)
        runtime_settings.use_web_interface = global_settings.cfg.getboolean(C_WEB_INT, P_WEB_ENABLE, fallback=False)
        runtime_settings.max_logs = global_settings.cfg[C_LOGGING][P_LOG_MAX]
        runtime_settings.cmd_queue_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_QUEUE_LIM])
        runtime_settings.cmd_hist_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_HIST_LIM])
        if len(runtime_settings.cmd_token) != 1:
            print("ERROR: The command token must be a single character! Reverting to the default: '!' token.")
            runtime_settings.cmd_token = '!'

    @staticmethod
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

    @staticmethod
    def initialize_web():
        if not runtime_settings.use_web_interface:
            return
        import threading
        runtime_settings.web_ip = global_settings.cfg[C_WEB_INT][P_WEB_IP]
        runtime_settings.web_port = int(global_settings.cfg[C_WEB_INT][P_WEB_PORT])
        runtime_settings.web_thread = threading.Thread(target=web_service.start_server())
        runtime_settings.web_thread.start()

    @staticmethod
    def shutdown_web():
        if not runtime_settings.use_web_interface:
            return
        web_service.stop_server()
        runtime_settings.web_thread.join()

    # Initializes only safe-mode applicable plugins.
    # TODO: Re-introduce help plugin.
    # TODO: Require all plugins to come with metadata specifying initialization data requirements.
    @staticmethod
    def initialize_plugins_safe():
        import sys
        import os
        # Load Plugins
        rprint("######### Initializing Plugins - Safe Mode #########")
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins')
        all_imports = [name for name in os.listdir(f'{dir_utils.get_main_dir()}/plugins') if
                       os.path.isdir(
                           os.path.join(f'{dir_utils.get_main_dir()}/plugins', name)) and name != "__pycache__"]
        for p_file in all_imports:
            # if p_file == "help":
            #     continue
            if p_file == "bot_commands":
                global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
        # help_plugin = __import__('help.help')
        # self.bot_plugins['help'] = help_plugin.help.Plugin(self.bot_plugins)
        sys.path.pop(0)
        rprint("######### Plugins Initialized - Safe Mode #########")

    # Initializes all available plugins.
    # TODO: Re-introduce help plugin.
    # TODO: Require all plugins to come with metadata specifying initialization data requirements.
    @staticmethod
    def initialize_plugins():
        import sys
        import os

        global_settings.bot_plugins = {}
        # Load Core Plugins
        rprint("######### Initializing Core Plugins #########")
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins/core')
        all_imports = [name for name in os.listdir(f'{dir_utils.get_main_dir()}/plugins/core') if
                       os.path.isdir(os.path.join(f'{dir_utils.get_main_dir()}/plugins/core',
                                                  name)) and name != "__pycache__"]
        for p_file in all_imports:
            global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
        sys.path.pop(0)
        rprint("######### Core Plugins Initialized #########")
        # Load Extension Plugins
        rprint("######### Initializing Extension Plugins #########")
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins/extensions')
        all_imports = [name for name in os.listdir(f'{dir_utils.get_main_dir()}/plugins/extensions') if
                       os.path.isdir(
                           os.path.join(f'{dir_utils.get_main_dir()}/plugins/extensions',
                                        name)) and name != "__pycache__"]
        for p_file in all_imports:
            # if p_file == "youtube" or p_file == "help":
            #    continue
            global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
        sys.path.pop(0)
        rprint("######### Extension Plugins Initialized #########")
        # Import the help and youtube plugins separately.
        # help_plugin = __import__('help.help')
        # youtube_plugin = __import__('youtube.youtube')
        # Assign audio plugins manually.
        # self.bot_plugins['youtube'] = youtube_plugin.youtube.Plugin()
        # self.bot_plugins.get('youtube').set_sound_board_plugin(self.bot_plugins.get('sound_board'))
        # self.bot_plugins.get('sound_board').set_youtube_plugin(self.bot_plugins.get('youtube'))
        # self.bot_plugins['help'] = help_plugin.help.Plugin(self.bot_plugins)

    @staticmethod
    def log(level, message):
        if not runtime_settings.use_logging:
            return
        if not global_settings.log_service:
            return
        else:
            if level == INFO:
                global_settings.log_service.info(message)
            elif level == DEBUG:
                global_settings.log_service.debug(message)
            elif level == WARNING:
                global_settings.log_service.warning(message)
            elif level == CRITICAL:
                global_settings.log_service.critical(message)


