from JJMumbleBot.settings import global_settings
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.lib.mumble_data import MumbleData
from JJMumbleBot.lib.utils.database_management_utils import get_memory_db, save_memory_db_to_file
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.database_utils import InsertDB, UtilityDB, DeleteDB
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.callbacks import Callbacks, CommandCallbacks, CoreCallbacks


class BotServiceHelper:
    @staticmethod
    def retrieve_mumble_data(serv_ip, serv_port, serv_pass):
        server_ip: str = serv_ip
        server_port: int = serv_port
        server_pass: str = serv_pass
        user_id: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID]
        user_cert: str = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_CERT]
        use_stereo: bool = global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_USE_STEREO, fallback=True)
        use_reconnect: bool = global_settings.cfg.getboolean(C_CONNECTION_SETTINGS, P_SERVER_RECONNECT, fallback=False)
        return MumbleData(ip=server_ip, port=server_port, uid=user_id, pwd=server_pass, cert=user_cert,
                          stereo=use_stereo, reconnect=use_reconnect)

    @staticmethod
    def initialize_settings():
        global_settings.mtd_callbacks = Callbacks()
        global_settings.cmd_callbacks = CommandCallbacks()
        global_settings.plugin_callbacks = Callbacks()
        global_settings.core_callbacks = CoreCallbacks()

        runtime_settings.tick_rate = float(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TICK_RATE])
        runtime_settings.cmd_hist_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_MULTI_LIM])
        runtime_settings.cmd_token = global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]
        runtime_settings.use_logging = global_settings.cfg.getboolean(C_LOGGING, P_LOG_ENABLE, fallback=False)
        runtime_settings.max_logs = int(global_settings.cfg[C_LOGGING][P_LOG_MAX])
        runtime_settings.max_log_size = int(global_settings.cfg[C_LOGGING][P_LOG_SIZE_MAX])
        runtime_settings.log_trace = global_settings.cfg.getboolean(C_LOGGING, P_LOG_TRACE, fallback=False)
        runtime_settings.cmd_queue_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_QUEUE_LIM])
        runtime_settings.cmd_hist_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_HIST_LIM])
        runtime_settings.can_duck = global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_DUCK_AUDIO, fallback=False)
        if len(runtime_settings.cmd_token) != 1:
            log(ERROR, "The command token must be a single character! Reverting to the default: '!' token.",
                origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
            runtime_settings.cmd_token = '!'

    # Initializes only safe-mode applicable plugins.
    @staticmethod
    def initialize_plugins_safe():
        import sys
        from os import path, listdir
        from json import loads
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
        safe_mode_plugins = loads(global_settings.cfg.get(C_PLUGIN_SETTINGS, P_PLUG_SAFE))
        # Load Core Plugins
        log(INFO, "######### Initializing Core Plugins - Safe Mode #########",
            origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins/core')
        all_imports = [name for name in listdir(f'{dir_utils.get_main_dir()}/plugins/core') if
                       path.isdir(
                           path.join(f'{dir_utils.get_main_dir()}/plugins/core', name)) and name != "__pycache__"]
        for p_file in all_imports:
            if p_file in safe_mode_plugins:
                if not path.exists(f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/metadata.ini'):
                    log(WARNING, f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...",
                        origin=L_STARTUP, print_mode=PrintMode.VERBOSE_PRINT.value)
                    continue
                # Import the core plugin class.
                global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin

                # Register plugin command callbacks.
                plugin_metadata = PluginUtilityService.process_metadata(f'plugins/core/{p_file}')
                plugin_cmds = loads(plugin_metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
                for plugin_command in plugin_cmds:
                    global_settings.cmd_callbacks.register_command(f'{plugin_command}', p_file,
                                                                   f'{plugin_command}_clbk')
                    global_settings.mtd_callbacks.register_callback(
                        f'{plugin_command}_clbk',
                        getattr(
                            global_settings.bot_plugins[p_file],
                            f'cmd_{plugin_command}',
                            None
                        )
                    )
                    log(INFO,
                        f"Registered plugin command: {plugin_command}:{global_settings.cmd_callbacks.get_command(plugin_command)[1]}:cmd_{plugin_command}",
                        origin=L_STARTUP, print_mode=PrintMode.VERBOSE_PRINT.value)
                # Initialize the core plugin class instance.
                global_settings.bot_plugins[p_file] = global_settings.bot_plugins[p_file]()
                # Import core plugin into the database.
                InsertDB.insert_new_plugin(db_conn=get_memory_db(), plugin_name=p_file, ignore_file_save=True)
                # Import core plugin user privileges into the database.
                UtilityDB.import_privileges_to_db(db_conn=get_memory_db(),
                                                  csv_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/privileges.csv')
                # Import plugin aliases into the database.
                UtilityDB.import_aliases_to_db(db_conn=get_memory_db(),
                                               csv_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/aliases.csv')
                # Import plugin help into the database.
                UtilityDB.import_help_to_db(db_conn=get_memory_db(),
                                            html_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/help.html')
                # Create directory for user modifiable plugin-specific data and configs.
                dir_utils.make_directory(f'{dir_utils.get_plugin_data_dir()}/{p_file}')
        sys.path.pop(0)
        log(INFO, "######### Core Plugins Initialized - Safe Mode #########",
            origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
        # Load Extension Plugins
        log(INFO, "######### Initializing Extension Plugins - Safe Mode #########",
            origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins/extensions')
        all_imports = [name for name in listdir(f'{dir_utils.get_main_dir()}/plugins/extensions') if
                       path.isdir(
                           path.join(f'{dir_utils.get_main_dir()}/plugins/extensions',
                                     name)) and name != "__pycache__"]
        for p_file in all_imports:
            if p_file in safe_mode_plugins:
                if not path.exists(path.join(f'{dir_utils.get_main_dir()}/plugins/extensions',
                                             p_file)):
                    log(WARNING, f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...",
                        origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
                    continue
                # Import the core plugin class.
                global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin

                # Register plugin command callbacks.
                plugin_metadata = PluginUtilityService.process_metadata(f'plugins/core/{p_file}')
                plugin_cmds = loads(plugin_metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
                for plugin_command in plugin_cmds:
                    global_settings.cmd_callbacks.register_command(f'{plugin_command}', p_file,
                                                                   f'{plugin_command}_clbk')
                    global_settings.mtd_callbacks.register_callback(
                        f'{plugin_command}_clbk',
                        getattr(
                            global_settings.bot_plugins[p_file],
                            f'cmd_{plugin_command}',
                            None
                        )
                    )
                    log(INFO,
                        f"Registered plugin command: {plugin_command}:{global_settings.cmd_callbacks.get_command(plugin_command)[1]}:cmd_{plugin_command}",
                        origin=L_STARTUP, print_mode=PrintMode.VERBOSE_PRINT.value)
                # Initialize the core plugin class instance.
                global_settings.bot_plugins[p_file] = global_settings.bot_plugins[p_file]()
                # Import core plugin into the database.
                InsertDB.insert_new_plugin(db_conn=get_memory_db(), plugin_name=p_file, ignore_file_save=True)
                # Import core plugin user privileges into the database.
                UtilityDB.import_privileges_to_db(db_conn=get_memory_db(),
                                                  csv_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/privileges.csv')
                # Import plugin aliases into the database.
                UtilityDB.import_aliases_to_db(db_conn=get_memory_db(),
                                               csv_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/aliases.csv')
                # Import plugin help into the database.
                UtilityDB.import_help_to_db(db_conn=get_memory_db(),
                                            html_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/help.html')
                # Create directory for user modifiable plugin-specific data and configs.
                dir_utils.make_directory(f'{dir_utils.get_plugin_data_dir()}/{p_file}')
        save_memory_db_to_file()
        sys.path.pop(0)
        log(INFO, "######### Extension Plugins Initialized - Safe Mode #########",
            origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)

    # Initializes all available plugins.
    @staticmethod
    def initialize_plugins():
        import sys
        from os import path, listdir
        from json import loads

        # Clear plugins, plugins_help, and commands tables on launch.
        DeleteDB.delete_all_commands(db_conn=get_memory_db())
        DeleteDB.delete_all_plugins_help(db_conn=get_memory_db())
        DeleteDB.delete_all_plugins(db_conn=get_memory_db())

        # Import global aliases into the database.
        UtilityDB.import_aliases_to_db(db_conn=get_memory_db(),
                                       csv_path=f'{dir_utils.get_main_dir()}/cfg/global_aliases.csv')

        global_settings.bot_plugins = {}
        # Load Core Plugins
        log(INFO, "######### Initializing Core Plugins #########",
            origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins/core')
        all_imports = [name for name in listdir(f'{dir_utils.get_main_dir()}/plugins/core') if
                       path.isdir(path.join(f'{dir_utils.get_main_dir()}/plugins/core',
                                            name)) and name != "__pycache__"]
        for p_file in all_imports:
            if not path.exists(f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/metadata.ini'):
                log(WARNING, f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...",
                    origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
                continue
            # Import the core plugin class.
            global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin

            # Register plugin command callbacks.
            plugin_metadata = PluginUtilityService.process_metadata(f'plugins/core/{p_file}')
            plugin_cmds = loads(plugin_metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
            for plugin_command in plugin_cmds:
                global_settings.cmd_callbacks.register_command(f'{plugin_command}', p_file,
                                                               f'{plugin_command}_clbk')
                global_settings.mtd_callbacks.register_callback(
                    f'{plugin_command}_clbk',
                    getattr(
                        global_settings.bot_plugins[p_file],
                        f'cmd_{plugin_command}',
                        None
                    )
                )
                log(INFO, f"Registered plugin command: "
                       f"{plugin_command}:{global_settings.cmd_callbacks.get_command(plugin_command)[1]}:cmd_{plugin_command}",
                    origin=L_STARTUP, print_mode=PrintMode.VERBOSE_PRINT.value)
            # Initialize the core plugin class instance.
            global_settings.bot_plugins[p_file] = global_settings.bot_plugins[p_file]()

            # Import core plugin into the database.
            InsertDB.insert_new_plugin(db_conn=get_memory_db(), plugin_name=p_file, ignore_file_save=True)
            # Import core plugin user privileges into the database.
            UtilityDB.import_privileges_to_db(db_conn=get_memory_db(),
                                              csv_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/privileges.csv')
            # Import plugin aliases into the database.
            UtilityDB.import_aliases_to_db(db_conn=get_memory_db(),
                                           csv_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/aliases.csv')
            # Import plugin help into the database.
            UtilityDB.import_help_to_db(db_conn=get_memory_db(),
                                        html_path=f'{dir_utils.get_main_dir()}/plugins/core/{p_file}/help.html')
            # Create directory for user modifiable plugin-specific data and configs.
            dir_utils.make_directory(f'{dir_utils.get_plugin_data_dir()}/{p_file}')
        sys.path.pop(0)
        log(INFO, "######### Core Plugins Initialized #########",
            origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
        # Load Extension Plugins
        log(INFO, "######### Initializing Extension Plugins #########",
            origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
        sys.path.insert(0, f'{dir_utils.get_main_dir()}/plugins/extensions')
        all_imports = [name for name in listdir(f'{dir_utils.get_main_dir()}/plugins/extensions') if
                       path.isdir(
                           path.join(f'{dir_utils.get_main_dir()}/plugins/extensions',
                                     name)) and name != "__pycache__"]
        for p_file in all_imports:
            if not path.exists(f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/metadata.ini'):
                log(WARNING, f"{p_file} plugin does not contain a metadata.ini file. Skipping initialization...",
                    origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
                continue
            # Import the core plugin class.
            global_settings.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin

            # Register plugin command callbacks.
            plugin_metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{p_file}')
            plugin_cmds = loads(plugin_metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
            for plugin_command in plugin_cmds:
                global_settings.cmd_callbacks.register_command(f'{plugin_command}', p_file,
                                                               f'{plugin_command}_clbk')
                global_settings.mtd_callbacks.register_callback(
                    f'{plugin_command}_clbk',
                    getattr(
                        global_settings.bot_plugins[p_file],
                        f'cmd_{plugin_command}',
                        None
                    )
                )
                log(INFO,
                    f"Registered plugin command: {plugin_command}:{global_settings.cmd_callbacks.get_command(plugin_command)[1]}:cmd_{plugin_command}",
                    origin=L_STARTUP, print_mode=PrintMode.VERBOSE_PRINT.value)
            # Initialize the core plugin class instance.
            global_settings.bot_plugins[p_file] = global_settings.bot_plugins[p_file]()
            # Import core plugin into the database.
            InsertDB.insert_new_plugin(db_conn=get_memory_db(), plugin_name=p_file, ignore_file_save=True)
            # Import core plugin user privileges into the database.
            UtilityDB.import_privileges_to_db(db_conn=get_memory_db(),
                                              csv_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/privileges.csv')
            # Import plugin aliases into the database.
            UtilityDB.import_aliases_to_db(db_conn=get_memory_db(),
                                           csv_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/aliases.csv')
            # Import plugin help into the database.
            UtilityDB.import_help_to_db(db_conn=get_memory_db(),
                                        html_path=f'{dir_utils.get_main_dir()}/plugins/extensions/{p_file}/help.html')
            # Create directory for user modifiable plugin-specific data and configs.
            dir_utils.make_directory(f'{dir_utils.get_plugin_data_dir()}/{p_file}')
        save_memory_db_to_file()
        sys.path.pop(0)
        log(INFO, "######### Extension Plugins Initialized #########",
            origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)

    @staticmethod
    def backup_database():
        from datetime import datetime
        from shutil import copy
        from os import path, makedirs
        if not path.exists(f'{dir_utils.get_main_dir()}/cfg/backups'):
            makedirs(f'{dir_utils.get_main_dir()}/cfg/backups')
        if not path.exists(f'{dir_utils.get_main_dir()}/cfg/jjmumblebot.db'):
            return None
        cur_time = str(datetime.now())[:19].replace(":", "_").replace(" ", "")
        src_file = f'{dir_utils.get_main_dir()}/cfg/jjmumblebot.db'
        dst_file = f'{dir_utils.get_main_dir()}/cfg/backups/jjmumblebot_{str(cur_time)}.db'
        copy(src_file, dst_file)
        return dst_file
