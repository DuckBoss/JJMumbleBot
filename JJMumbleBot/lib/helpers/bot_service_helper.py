from JJMumbleBot.settings import global_settings
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.lib.mumble_data import MumbleData
from JJMumbleBot.lib.utils.database_management_utils import get_memory_db, save_memory_db_to_file
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.database_utils import InsertDB, UtilityDB
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.callbacks import Callbacks, CommandCallbacks


class BotServiceHelper:
    @staticmethod
    def retrieve_mumble_data():
        server_ip: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_IP]
        server_pass: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_PASS]
        server_port: int = int(global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_PORT])
        user_id: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID]
        user_cert: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_CERT]
        use_stereo: bool = global_settings.cfg.getboolean(C_MAIN_SETTINGS, P_AUD_STEREO)
        return MumbleData(ip=server_ip, port=server_port, uid=user_id, pwd=server_pass, cert=user_cert,
                          stereo=use_stereo)

    @staticmethod
    def initialize_settings():
        import configparser
        global_settings.cfg = configparser.ConfigParser()
        global_settings.cfg.read(f"{dir_utils.get_main_dir()}/cfg/config.ini")
        global_settings.all_callbacks = Callbacks()
        global_settings.cmd_callbacks = CommandCallbacks()

        runtime_settings.tick_rate = float(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TICK_RATE])
        runtime_settings.cmd_hist_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_MULTI_LIM])
        runtime_settings.cmd_token = global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]
        runtime_settings.use_logging = global_settings.cfg.getboolean(C_LOGGING, P_LOG_ENABLE, fallback=False)
        runtime_settings.max_logs = global_settings.cfg[C_LOGGING][P_LOG_MAX]
        runtime_settings.cmd_queue_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_QUEUE_LIM])
        runtime_settings.cmd_hist_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_HIST_LIM])
        if len(runtime_settings.cmd_token) != 1:
            rprint("ERROR: The command token must be a single character! Reverting to the default: '!' token.")
            runtime_settings.cmd_token = '!'

    # Initializes only safe-mode applicable plugins.
    @staticmethod
    def initialize_plugins_safe():
        import sys
        import os
        import json
        from JJMumbleBot.lib.resources.strings import C_PLUGIN_SETTINGS, P_PLUG_SAFE
        if not global_settings.cfg:
            from JJMumbleBot.lib.errors import ExitCodes, ConfigError
            from JJMumbleBot.lib.utils import runtime_utils
            runtime_utils.exit_bot_error(ExitCodes.CONFIG_ERROR)
            raise ConfigError('There was an error loading the global config for initializing safe mode plugins.')

        # Import global aliases into the database.
        UtilityDB.import_aliases_to_db(db_conn=get_memory_db(),
                                       csv_path=f'{dir_utils.get_main_dir()}/cfg/global_aliases.csv')

        global_settings.bot_plugins = {}
        safe_mode_plugins = json.loads(global_settings.cfg.get(C_PLUGIN_SETTINGS, P_PLUG_SAFE))
        # Load Core Plugins
        rprint("######### Initializing Core Plugins - Safe Mode #########")
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins/core')
        all_imports = [name for name in os.listdir(f'{dir_utils.get_main_dir()}/plugins/core') if
                       os.path.isdir(
                           os.path.join(f'{dir_utils.get_main_dir()}/plugins/core', name)) and name != "__pycache__"]
        for p_file in all_imports:
            if p_file in safe_mode_plugins:
                if not os.path.exists(os.path.join(f'{dir_utils.get_main_dir()}/plugins/core',
                                                   p_file)):
                    rprint(f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...")
                    log(WARNING, f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...")
                    continue
                # Import the core plugin.
                global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
                # Import core plugin into the database.
                InsertDB.insert_new_plugin(db_conn=get_memory_db(), plugin_name=p_file, ignore_file_save=True)
                # Import core plugin user privileges into the database.
                UtilityDB.import_privileges_to_db(db_conn=get_memory_db(), csv_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/privileges.csv')
                # Import plugin aliases into the database.
                UtilityDB.import_aliases_to_db(db_conn=get_memory_db(), csv_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/aliases.csv')
                # Import plugin help into the database.
                UtilityDB.import_help_to_db(db_conn=get_memory_db(), html_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/help.html')
        # help_plugin = __import__('help.help')
        # self.bot_plugins['help'] = help_plugin.help.Plugin(self.bot_plugins)
        sys.path.pop(0)
        rprint("######### Core Plugins Initialized - Safe Mode #########")
        # Load Extension Plugins
        rprint("######### Initializing Extension Plugins - Safe Mode #########")
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins/extensions')
        all_imports = [name for name in os.listdir(f'{dir_utils.get_main_dir()}/plugins/extensions') if
                       os.path.isdir(
                           os.path.join(f'{dir_utils.get_main_dir()}/plugins/extensions',
                                        name)) and name != "__pycache__"]
        for p_file in all_imports:
            if p_file in safe_mode_plugins:
                if not os.path.exists(os.path.join(f'{dir_utils.get_main_dir()}/plugins/extensions',
                                                   p_file)):
                    rprint(f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...")
                    log(WARNING, f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...")
                    continue
                # Import the core plugin.
                global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
                # Import core plugin into the database.
                InsertDB.insert_new_plugin(db_conn=get_memory_db(), plugin_name=p_file, ignore_file_save=True)
                # Import core plugin user privileges into the database.
                UtilityDB.import_privileges_to_db(db_conn=get_memory_db(), csv_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/privileges.csv')
                # Import plugin aliases into the database.
                UtilityDB.import_aliases_to_db(db_conn=get_memory_db(), csv_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/aliases.csv')
                # Import plugin help into the database.
                UtilityDB.import_help_to_db(db_conn=get_memory_db(), html_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/help.html')
        save_memory_db_to_file()
        sys.path.pop(0)
        rprint("######### Extension Plugins Initialized - Safe Mode #########")

    # Initializes all available plugins.
    @staticmethod
    def initialize_plugins():
        import sys
        import os

        # Import global aliases into the database.
        UtilityDB.import_aliases_to_db(db_conn=get_memory_db(),
                                       csv_path=f'{dir_utils.get_main_dir()}/cfg/global_aliases.csv')

        global_settings.bot_plugins = {}
        # Load Core Plugins
        rprint("######### Initializing Core Plugins #########")
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins/core')
        all_imports = [name for name in os.listdir(f'{dir_utils.get_main_dir()}/plugins/core') if
                       os.path.isdir(os.path.join(f'{dir_utils.get_main_dir()}/plugins/core',
                                                  name)) and name != "__pycache__"]
        for p_file in all_imports:
            if not os.path.exists(os.path.join(f'{dir_utils.get_main_dir()}/plugins/core',
                                               p_file)):
                rprint(f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...")
                log(WARNING, f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...")
                continue
            # Import the core plugin.
            global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
            # Import core plugin into the database.
            InsertDB.insert_new_plugin(db_conn=get_memory_db(), plugin_name=p_file, ignore_file_save=True)
            # Import core plugin user privileges into the database.
            UtilityDB.import_privileges_to_db(db_conn=get_memory_db(), csv_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/privileges.csv')
            # Import plugin aliases into the database.
            UtilityDB.import_aliases_to_db(db_conn=get_memory_db(), csv_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/aliases.csv')
            # Import plugin help into the database.
            UtilityDB.import_help_to_db(db_conn=get_memory_db(), html_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/help.html')
            # Register plugin command callbacks.
            for plugin in global_settings.bot_plugins[p_file]:
                for plugin_command in plugin.plugin_cmds:
                    global_settings.cmd_callbacks.register_command(f'{plugin_command}', f'on_{plugin_command}')
                    global_settings.all_callbacks.register_callback(f'on_{plugin_command}', f'on_{plugin_command}')
                    rprint(f"Registered plugin command: {plugin_command}-on_{plugin_command}")
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
            if not os.path.exists(os.path.join(f'{dir_utils.get_main_dir()}/plugins/extensions',
                                               p_file)):
                rprint(f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...")
                log(WARNING, f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...")
                continue
            # Import the core plugin.
            global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
            # Import core plugin into the database.
            InsertDB.insert_new_plugin(db_conn=get_memory_db(), plugin_name=p_file, ignore_file_save=True)
            # Import core plugin user privileges into the database.
            UtilityDB.import_privileges_to_db(db_conn=get_memory_db(), csv_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/privileges.csv')
            # Import plugin aliases into the database.
            UtilityDB.import_aliases_to_db(db_conn=get_memory_db(), csv_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/aliases.csv')
            # Import plugin help into the database.
            UtilityDB.import_help_to_db(db_conn=get_memory_db(), html_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/help.html')
        save_memory_db_to_file()
        sys.path.pop(0)
        rprint("######### Extension Plugins Initialized #########")

    @staticmethod
    def backup_database():
        from datetime import datetime
        from shutil import copy
        from os import path, makedirs
        if not path.exists(f'{dir_utils.get_main_dir()}/cfg/backups'):
            makedirs(f'{dir_utils.get_main_dir()}/cfg/backups')
        cur_time = str(datetime.now())[:19].replace(":", "_").replace(" ", "")
        src_file = f'{dir_utils.get_main_dir()}/cfg/jjmumblebot.db'
        dst_file = f'{dir_utils.get_main_dir()}/cfg/backups/jjmumblebot_{str(cur_time)}.db'
        copy(src_file, dst_file)
        return dst_file
