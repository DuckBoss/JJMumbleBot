import pymumble.pymumble_py3 as pymumble
import time
import os
import sys
import utils
import privileges as pv
import aliases
import logging
from logging.handlers import TimedRotatingFileHandler
from pgui import PseudoGUI
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print, reg_print
from helpers.queue_handler import QueueHandler
from helpers.command import Command
from helpers.cmd_history import CMDQueue
from bs4 import BeautifulSoup
import threading
import copy


class JJMumbleBot:
    # Toggles for bot states.
    exit_flag = False
    # Bot status.
    bot_status = "Offline"
    # Dictionary of registered bot plugins.
    bot_plugins = {}
    # Command history.
    cmd_history = None
    # Runtime parameters.
    tick_rate = 0.1
    multi_cmd_limit = 5
    cmd_token = None
    priv_path = "bot_commands/bot_commands_privileges.csv"

    def __init__(self):
        print("JJ Mumble Bot Initializing...")
        # Initialize configs.
        GM.cfg.read(utils.get_config_dir())
        # Initialize application logging.
        logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)

        log_file_name = f"{GM.cfg['Bot_Directories']['LogDirectory']}/runtime.log"
        GM.logger = logging.getLogger("RuntimeLogging")
        GM.logger.setLevel(logging.DEBUG)
   
        handler = TimedRotatingFileHandler(log_file_name, when='midnight', backupCount=30)
        handler.setLevel(logging.INFO)
        log_formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        handler.setFormatter(log_formatter)
        GM.logger.addHandler(handler)

        GM.logger.info("######################################")
        GM.logger.info("Initializing JJMumbleBot...")
        GM.logger.info("Application configs have been read successfully.")
        # Initialize system arguments.
        if sys.argv:
            for item in sys.argv:
                # Enable safe mode.
                if item == "-safe":
                    GM.safe_mode = True
                    print('Safe mode has been enabled.')
                    GM.logger.info("Safe mode has been enabled through system arguments.")
                # Enable debug mode.
                if item == "-debug":
                    GM.debug_mode = True
                    print('Debug mode has been enabled.')
                    GM.logger.info("Debug mode has been enabled through system arguments.")
                # Enable quiet mode.
                if item == "-quiet":
                    GM.quiet_mode = True
                    print('Quiet mode has been enabled.')
                    GM.logger.info("Quiet mode has been enabled through system arguments.")
                # Enable verbose mode.
                if item == "-verbose":
                    GM.verbose_mode = True
                    print('Verbose mode has been enabled.')
                    GM.logger.info("Verbose mode has been enabled through system arguments.")
        # Initialize command queue.
        cmd_queue_lim = int(GM.cfg['Main_Settings']['CommandQueueLimit'])
        self.command_queue = QueueHandler(cmd_queue_lim)
        # Initialize command history tracker.
        cmd_history_lim = int(GM.cfg['Main_Settings']['CommandHistoryLimit'])
        self.cmd_history = CMDQueue(cmd_history_lim)
        # Run Debug Mode tests.
        if GM.debug_mode:
            self.config_debug()
        # Retrieve mumble client data from configs.
        server_ip = GM.cfg['Connection_Settings']['ServerIP']
        server_pass = GM.cfg['Connection_Settings']['ServerPassword']
        server_port = int(GM.cfg['Connection_Settings']['ServerPort'])
        user_id = GM.cfg['Connection_Settings']['UserID']
        user_cert = GM.cfg['Connection_Settings']['UserCertification']
        GM.logger.info("Retrieved server information from application configs.")
        # Set main logic loop tick rate.
        self.tick_rate = float(GM.cfg['Main_Settings']['CommandTickRate'])
        # Set multi-command limit.
        self.multi_cmd_limit = int(GM.cfg['Main_Settings']['MultiCommandLimit'])
        # Set the command token.
        self.cmd_token = GM.cfg['Main_Settings']['CommandToken']
        if len(self.cmd_token) != 1:
            print("ERROR: The command token must be a single character! Reverting to the default: '!' token.")
            GM.logger.critical("ERROR: The command token must be a single character! Reverting to the default: '!' token.")
            self.cmd_token = '!'
        # Initialize mumble client.
        self.mumble = pymumble.Mumble(server_ip, user=user_id, port=server_port, certfile=user_cert,
                                      password=server_pass)
        # Initialize mumble callbacks.
        self.mumble.callbacks.set_callback("text_received", self.message_received)
        # Set mumble codec profile.
        self.mumble.set_codec_profile("audio")
        # Create temporary directories.
        utils.make_directory(GM.cfg['Media_Directories']['TemporaryImageDirectory'])
        GM.logger.info("Initialized temporary directories.")
        # Create any missing permanent directories.
        utils.make_directory(GM.cfg['Media_Directories']['PermanentMediaDirectory']+"sound_board/")
        utils.make_directory(GM.cfg['Media_Directories']['PermanentMediaDirectory']+"images/")
        GM.logger.info("Initialized permanent directories.")
        # Setup privileges.
        pv.setup_privileges()
        GM.logger.info("Initialized user privileges.")
        # Setup aliases.
        aliases.setup_aliases()
        GM.logger.info("Initialized aliases.")
        # Initialize PGUI.
        GM.gui = PseudoGUI(self.mumble)
        GM.logger.info("Initialized pseudo graphical user interface.")
        # Initialize plugins.
        if GM.safe_mode:
            self.initialize_plugins_safe()
            GM.logger.info("Initialized plugins with safe mode.")
        else:
            self.initialize_plugins()
            GM.logger.info("Initialized plugins.")
        # Run a plugin callback test.
        self.plugin_callback_test()
        GM.logger.info("Plugin callback test successful.")
        print("JJ Mumble Bot initialized!\n")
        # Join the server after all initialization is complete.
        self.join_server()
        GM.logger.info("JJ Mumble Bot has fully initialized and joined the server.")
        self.loop()

    # Prints all the contents of the config.ini file.
    def config_debug(self):
        print("\n-------------------------------------------")
        print("Config Debug:")
        for sect in GM.cfg.sections():
            print(f"[{sect}]")
            for (key, val) in GM.cfg.items(sect):
                print(f"{key}={val}")
        print("-------------------------------------------\n")

    # Initializes only safe-mode applicable plugins.
    def initialize_plugins_safe(self):
        # Load Plugins
        reg_print("######### Initializing Plugins #########")
        sys.path.insert(0, utils.get_plugin_dir())
        all_imports = [name for name in os.listdir(utils.get_plugin_dir()) if
                       os.path.isdir(os.path.join(utils.get_plugin_dir(), name))]
        for p_file in all_imports:
            if p_file == "help":
                continue
            elif p_file == "bot_commands" or p_file == "uptime":
                self.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
        help_plugin = __import__('help.help')
        self.bot_plugins['help'] = help_plugin.Plugin(self.bot_plugins)
        sys.path.pop(0)
        reg_print("######### Plugins Initialized #########")

    # Initializes all available plugins.
    def initialize_plugins(self):
        # Load Plugins
        reg_print("######### Initializing Plugins #########")
        sys.path.insert(0, utils.get_plugin_dir())
        all_imports = [name for name in os.listdir(utils.get_plugin_dir()) if os.path.isdir(os.path.join(utils.get_plugin_dir(), name)) and name != "__pycache__"]
        for p_file in all_imports:
            if p_file == "youtube" or p_file == "help":
                continue
            self.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
        # Import the help and youtube plugins separately.
        help_plugin = __import__('help.help')
        youtube_plugin = __import__('youtube.youtube')
        # Assign audio plugins manually.
        self.bot_plugins['youtube'] = youtube_plugin.youtube.Plugin()
        self.bot_plugins.get('youtube').set_sound_board_plugin(self.bot_plugins.get('sound_board'))
        self.bot_plugins.get('sound_board').set_youtube_plugin(self.bot_plugins.get('youtube'))
        self.bot_plugins['help'] = help_plugin.help.Plugin(self.bot_plugins)
        sys.path.pop(0)
        reg_print("######### Plugins Initialized #########")

    # Runs a check to add any new plugins that have been detected at runtime.
    def live_plugin_check(self):
        if GM.safe_mode:
            length_check = 3
        else:
            length_check = len([f for f in os.listdir(utils.get_plugin_dir()) if f != "__pycache__"])
        if length_check != len(self.bot_plugins):
            reg_print("Plugin change detected... adding to plugin cache.")
            GM.logger.warning("Plugin change detected... adding to plugin cache.")
            self.refresh_plugins()

    # A callback test that prints out the test outputs of all the registered plugins.
    def plugin_callback_test(self):
        # Plugin Callback Tests
        reg_print("######### Running plugin callback tests #########")
        for plugin in self.bot_plugins.values():
            plugin.plugin_test()
        reg_print("######### Plugin callback tests complete #########")

    # Refreshes all active plugins by quitting out of them completely and restarting them.
    def refresh_plugins(self):
        reg_print("Refreshing all plugins...")
        # utils.echo(utils.get_my_channel(self.mumble),
        #           f"{utils.get_bot_name()} is refreshing all plugins.")
        GM.gui.quick_gui(
            f"{utils.get_bot_name()} is refreshing all plugins.",
            text_type='header',
            box_align='left')
        for plugin in self.bot_plugins.values():
            plugin.quit()
        self.bot_plugins.clear()
        if GM.safe_mode:
            self.initialize_plugins_safe()
        else:
            self.initialize_plugins()
        pv.setup_privileges()
        reg_print("All plugins refreshed.")
        # utils.echo(utils.get_my_channel(self.mumble),
        #           f"{utils.get_bot_name()} has refreshed all plugins.")
        GM.gui.quick_gui(
            f"{utils.get_bot_name()} has refreshed all plugins.",
            text_type='header',
            box_align='left')
        GM.logger.info("JJ Mumble Bot has refreshed all plugins.")

    def join_server(self):
        self.mumble.start()
        self.mumble.is_ready()
        self.bot_status = "Online"
        self.mumble.users.myself.comment(
            f"This is {utils.get_bot_name()} [{utils.get_version()}].<br>{utils.get_known_bugs()}<br>")
        self.mumble.set_bandwidth(192000)
        self.mumble.channels.find_by_name(utils.get_default_channel()).move_in()
        utils.mute(self.mumble)
        self.mumble.channels[self.mumble.users.myself['channel_id']].send_text_message(f"{utils.get_bot_name()} is Online.")
        reg_print(f"\nJJMumbleBot is {self.status()}\n")

    def status(self):
        return self.bot_status

    def message_received(self, text):
        message = text.message.strip()
        user = self.mumble.users[text.actor]
        if "<img" in message:
            reg_print(f"Message Received: [{user['name']} -> Image Data]")
        elif "<a href=" in message:
            reg_print(f"Message Received: [{user['name']} -> Hyperlink Data]")
        else:
            reg_print(f"Message Received: [{user['name']} -> {message}]")

        if message[0] == self.cmd_token:
            GM.logger.info(f"Commands Received: [{user['name']} -> {message}]")
            self.live_plugin_check()

            # example input: !version ; !about ; !yt twice ; !p ; !status
            all_commands = [msg.strip() for msg in message.split(';')]
            # example output: ["!version", "!about", "!yt twice", "!p", "!status"]

            # add to command history
            cmd_list = [self.cmd_history.insert(cmd) for cmd in all_commands]

            if len(all_commands) > self.multi_cmd_limit:
                reg_print(f"The multi-command limit was reached! The multi-command limit is {self.multi_cmd_limit} commands per line.")
                GM.logger.warning(f"The multi-command limit was reached! The multi-command limit is {self.multi_cmd_limit} commands per line.")
                return

            # Iterate through all commands provided and generate commands.
            for i, item in enumerate(all_commands):
                # Generate command with parameters
                new_text = copy.deepcopy(text)
                new_text.message = item
                new_command = None
                try:
                    new_command = Command(item[1:].split()[0], new_text)
                except IndexError:
                    continue

                if new_command.command in aliases.aliases:
                    alias_commands = [msg.strip() for msg in aliases.aliases[new_command.command].split('|')]
                    if len(alias_commands) > self.multi_cmd_limit:
                        reg_print(
                            f"The multi-command limit was reached! The multi-command limit is {self.multi_cmd_limit} commands per line.")
                        GM.logger.warning(
                            f"The multi-command limit was reached! The multi-command limit is {self.multi_cmd_limit} commands per line.")
                        return
                    for x, sub_item in enumerate(alias_commands):
                        sub_text = copy.deepcopy(text)
                        if len(item[1:].split()) > 1:
                            sub_text.message = f"{sub_item} {item[1:].split(' ', 1)[1]}"
                        else:
                            sub_text.message = sub_item

                        sub_command = None
                        try:
                            sub_command = Command(sub_item[1:].split()[0], sub_text)
                        except IndexError:
                            continue

                        self.command_queue.insert(sub_command)
                else:
                    # Insert command into the command queue
                    self.command_queue.insert(new_command)

            # Process commands if the queue is not empty
            while not self.command_queue.is_empty():
                # Process commands in the queue
                cur_cmd = self.command_queue.pop()
                thr = threading.Thread(target=self.process_command_queue, args=(cur_cmd,))
                thr.start()
                # Manually join the youtube plugin since the track-chooser can be overriden
                if cur_cmd.command == "yt" or cur_cmd.command == "youtube":
                    thr.join()
                # self.process_command_queue(cur_cmd)
                time.sleep(self.tick_rate)

    def process_core_commands(self, command, text):
        if command == "alias":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            message = text.message.strip()
            message_parse = message[1:].split(' ', 2)
            alias_name = message_parse[1]

            if alias_name in aliases.aliases.keys():
                aliases.set_alias(alias_name, message_parse[2])
                debug_print(f"Registered alias: [{alias_name}] - [{message_parse[2]}]")
                # utils.echo(utils.get_my_channel(self.mumble),
                #           f"Registered alias: [{alias_name}] - [{message_parse[2]}]")
                GM.gui.quick_gui(
                    f"Registered alias: [{alias_name}] - [{message_parse[2]}]",
                    text_type='header',
                    box_align='left')
            else:
                aliases.add_to_aliases(alias_name, message_parse[2])
                debug_print(f"Registered new alias: [{alias_name}] - [{message_parse[2]}]")
                # utils.echo(utils.get_my_channel(self.mumble),
                #           f"Registered new alias: [{alias_name}] - [{message_parse[2]}]")
                GM.gui.quick_gui(
                    f"Registered alias: [{alias_name}] - [{message_parse[2]}]",
                    text_type='header',
                    box_align='left')
            return

        elif command == "aliases":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            cur_text = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Registered Aliases:</font>"
            for i, alias in enumerate(aliases.aliases):
                cur_text += f"<br><font color={GM.cfg['PGUI_Settings']['IndexTextColor']}>[{alias}]</font> - [{BeautifulSoup(aliases.aliases[alias], 'html.parser').get_text()}]"
                if i % 50 == 0 and i != 0:
                    # utils.echo(utils.get_my_channel(self.mumble), cur_text)
                    GM.gui.quick_gui(
                        cur_text,
                        text_type='header',
                        box_align='left',
                        text_align='left')
                    cur_text = ""
            # utils.echo(utils.get_my_channel(self.mumble), cur_text)
            GM.gui.quick_gui(
                cur_text,
                text_type='header',
                box_align='left',
                text_align='left')
            return

        elif command == "removealias":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            message = text.message.strip()
            message_parse = message[1:].split(' ', 2)
            alias_name = message_parse[1]
            if aliases.remove_from_aliases(alias_name):
                debug_print(f'Removed [{alias_name}] from registered aliases.')
                # utils.echo(utils.get_my_channel(self.mumble),
                #           f'Removed [{alias_name}] from registered aliases.')
                GM.gui.quick_gui(
                    f'Removed [{alias_name}] from registered aliases.',
                    text_type='header',
                    box_align='left')
            else:
                debug_print(f'Could not remove [{alias_name}] from registered aliases.')
                # utils.echo(utils.get_my_channel(self.mumble),
                #           f'Could not remove [{alias_name}] from registered aliases.')
                GM.gui.quick_gui(
                    f'Could not remove [{alias_name}] from registered aliases.',
                    text_type='header',
                    box_align='left')
            return

        elif command == "clearaliases":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            if aliases.clear_aliases():
                debug_print('Cleared all registered aliases.')
                # utils.echo(utils.get_my_channel(self.mumble),
                #           'Cleared all registered aliases.')
                GM.gui.quick_gui(
                    'Cleared all registered aliases.',
                    text_type='header',
                    box_align='left')
            else:
                debug_print('The registered aliases could not be cleared.')
                # utils.echo(utils.get_my_channel(self.mumble),
                #           'The registered aliases could not be cleared.')
                GM.gui.quick_gui(
                    'The registered aliases could not be cleared.',
                    text_type='header',
                    box_align='left')
            return

        elif command == "refresh":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            self.refresh_plugins()
            return

        elif command == "sleep":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            sleep_time = float(text.message[1:].split(' ', 1)[1].strip())
            self.tick_rate = sleep_time
            time.sleep(sleep_time)
            self.tick_rate = float(GM.cfg['Main_Settings']['CommandTickRate'])
            return

        elif command == "exit":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            debug_print("Stopping all threads...")
            self.exit()
            GM.logger.info("JJ Mumble Bot is being shut down.")
            GM.logger.info("######################################")
            return

        elif command == "status":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            # utils.echo(utils.get_my_channel(self.mumble),
            #           f"{utils.get_bot_name()} is {self.status()}.")
            GM.gui.quick_gui(
                f"{utils.get_bot_name()} is {self.status()}.",
                text_type='header',
                box_align='left')
            return

        elif command == "version":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            # utils.echo(utils.get_my_channel(self.mumble),
            #           f"{utils.get_bot_name()} is on version {utils.get_version()}")
            GM.gui.quick_gui(
                f"{utils.get_bot_name()} is on version {utils.get_version()}",
                text_type='header',
                box_align='left')
            return

        elif command == "system_test":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            self.plugin_callback_test()
            debug_print("A system self-test was run.")
            GM.logger.info("A system self-test was run.")
            return

        elif command == "about":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            # utils.echo(utils.get_my_channel(self.mumble), utils.get_about())
            GM.gui.quick_gui(
                f"{utils.get_about()}<br>{utils.get_bot_name()} is on version {utils.get_version()}",
                text_type='header',
                box_align='left')
            return

        elif command == "history":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            cur_text = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Command History:</font>"
            for i, item in enumerate(self.cmd_history.queue_storage):
                cur_text += f"<br><font color={GM.cfg['PGUI_Settings']['IndexTextColor']}>[{i}]</font> - {item}"
                if i % 50 == 0 and i != 0:
                    # utils.echo(utils.get_my_channel(self.mumble), cur_text)
                    GM.gui.quick_gui(
                        cur_text,
                        text_type='header',
                        box_align='left',
                        text_align='left')
                    cur_text = ""
            # utils.echo(utils.get_my_channel(self.mumble), cur_text)
            GM.gui.quick_gui(
                cur_text,
                text_type='header',
                box_align='left',
                text_align='left')

        elif command == "reboot":
            if not pv.plugin_privilege_checker(self.mumble, text, command, self.priv_path):
                return
            self.exit()
            GM.logger.info("JJ Mumble Bot is being rebooted.")
            os.execv(sys.executable, ['python3'] + sys.argv)
            return

    def process_command_queue(self, com):
        command_type = com.command
        command_text = com.text
        self.process_core_commands(command_type, command_text)
        for plugin in self.bot_plugins.values():
            plugin.process_command(self.mumble, command_text)

    def exit(self):
        # utils.echo(utils.get_my_channel(self.mumble),
        #           f"{utils.get_bot_name()} was manually disconnected.")
        GM.gui.quick_gui(
            f"{utils.get_bot_name()} was manually disconnected.",
            text_type='header',
            box_align='left')
        for plugin in self.bot_plugins.values():
            plugin.quit()
        utils.clear_directory(utils.get_temporary_img_dir())
        reg_print("Cleared temporary directories.")
        self.exit_flag = True
        
    def loop(self):
        while not self.exit_flag:
            time.sleep(self.tick_rate)
