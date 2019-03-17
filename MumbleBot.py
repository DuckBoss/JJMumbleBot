import pymumble.pymumble_py3 as pymumble
import time
import os
import sys
import utils
import privileges as pv
import configparser
import logging

class Bot:
    exit_flag = False
    safe_mode = False
    debug_mode = False
    bot_status = "Offline"
    bot_plugins = {}
    cfg_inst = None

    def __init__(self):
        print("JJ Mumble Bot Initializing...")
        # Initialize configs.
        self.cfg_inst = configparser.ConfigParser()
        self.cfg_inst.read(utils.get_config_dir())
        # Initialize application logging.
        logging.basicConfig(filename='%s/runtime.log'%self.cfg_inst['Bot_Directories']['LogDirectory'], format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        logging.info("Application configs have been read succesfully.")
        # Initialize system arguments.
        if len(sys.argv) > 0:
            for item in sys.argv:
                # Enable safe mode.
                if item == "-safe":
                    self.safe_mode = True
                    logging.info("Safe mode has been enabled through system arguments.")
                if item == "-debug":
                    self.debug_mode = True
                    logging.info("Debug mode has been enabled through system arguments.")
        # Run Debug Mode tests.
        if self.debug_mode:
            self.config_debug()
        # Retrieve mumble client data from configs.
        server_ip = self.cfg_inst['Connection_Settings']['ServerIP']
        server_pass = self.cfg_inst['Connection_Settings']['ServerPassword']
        server_port = int(self.cfg_inst['Connection_Settings']['ServerPort'])
        user_id = self.cfg_inst['Connection_Settings']['UserID']
        user_cert = self.cfg_inst['Connection_Settings']['UserCertification']
        logging.info("Retrieved server information from application configs.")
        # Initialize mumble client.
        self.mumble = pymumble.Mumble(server_ip, user=user_id, port=server_port, certfile=user_cert,
                                      password=server_pass)
        # Initialize mumble callbacks.
        self.mumble.callbacks.set_callback("text_received", self.message_received)
        # Set mumble codec profile.
        self.mumble.set_codec_profile("audio")
        # Create temporary directories.
        utils.make_directory(self.cfg_inst['Media_Directories']['TemporaryMediaDirectory'])
        utils.make_directory(self.cfg_inst['Media_Directories']['TemporaryImageDirectory'])
        logging.info("Initialized temporary media directories.")
        # Setup privileges.
        utils.setup_privileges()
        logging.info("Initialized user privileges.")
        # Initialize plugins.
        if self.safe_mode:  
            self.initialize_plugins_safe()
            logging.info("Initialized plugins with safe mode.")
        else:
            self.initialize_plugins()
            logging.info("Initialized plugins.")
        # Run a plugin callback test.
        self.plugin_callback_test()
        logging.info("Plugin callback test succesful.")
        print("JJ Mumble Bot initialized!\n")
        # Join the server after all initialization is complete.
        self.join_server()
        logging.info("JJ Mumble Bot has fully initialized and joined the server.")
        self.loop()

    def config_debug(self):
        print("\n-------------------------------------------")
        print("Config Debug:")
        for sect in self.cfg_inst.sections():
            print("[%s]" % sect)
            for (key,val) in self.cfg_inst.items(sect):
                print("%s=%s" % (key, val))
        print("-------------------------------------------\n")

    def initialize_plugins_safe(self):
        # Load Plugins
        print("\n######### Initializing Plugins #########\n")
        sys.path.insert(0, self.cfg_inst['Bot_Directories']['PluginsDirectory'])
        for p_file in os.listdir(self.cfg_inst['Bot_Directories']['PluginsDirectory']):
            f_name, f_ext = os.path.splitext(p_file)
            if f_ext == ".py":
                if f_name == "help":
                    continue
                elif f_name == "bot_commands":
                    plugin = __import__(f_name)
                    self.bot_plugins[f_name] = plugin.Plugin()
        help_plugin = __import__('help')
        self.bot_plugins['help'] = help_plugin.Plugin(self.bot_plugins)
        sys.path.pop(0)

    def initialize_plugins(self):
        # Load Plugins
        print("\n######### Initializing Plugins #########\n")
        sys.path.insert(0, self.cfg_inst['Bot_Directories']['PluginsDirectory'])
        for p_file in os.listdir(self.cfg_inst['Bot_Directories']['PluginsDirectory']):
            f_name, f_ext = os.path.splitext(p_file)
            if f_ext == ".py":
                if f_name == "help" or f_name == "youtube":
                    continue
                else:
                    plugin = __import__(f_name)
                    self.bot_plugins[f_name] = plugin.Plugin()

        help_plugin = __import__('help')
        youtube_plugin = __import__('youtube')

        self.bot_plugins['youtube'] = youtube_plugin.Plugin(self.mumble)
        self.bot_plugins.get('youtube').set_sound_board_plugin(self.bot_plugins.get('sound_board'))
        self.bot_plugins.get('sound_board').set_youtube_plugin(self.bot_plugins.get('youtube'))
        self.bot_plugins['help'] = help_plugin.Plugin(self.bot_plugins)

        sys.path.pop(0)

    def live_plugin_check(self):
        length_check = len([f for f in os.listdir(self.cfg_inst['Bot_Directories']['PluginsDirectory']) if os.path.isfile(os.path.join(self.cfg_inst['Bot_Directories']['PluginsDirectory'], f))])
        if length_check != len(self.bot_plugins):
            print("Plugin change detected... adding to plugin cache.")
            logging.warning("Plugin change detected... adding to plugin cache.")
            self.refresh_plugins()

    def plugin_callback_test(self):
        # Plugin Callback Tests
        print("\n######### Running plugin callback tests #########\n")
        for plugin in self.bot_plugins.values():
            plugin.plugin_test()

    def refresh_plugins(self):
        print("Refreshing all plugins...")
        utils.echo(self.mumble.channels[self.mumble.users.myself['channel_id']],
                   "JJ Mumble Bot is refreshing all plugins.")
        time.sleep(0.3)
        print("Refreshing plugins...")
        for plugin in self.bot_plugins.values():
            plugin.quit()
        self.bot_plugins.clear()
        if self.safe_mode:
            self.initialize_plugins_safe()
        else:
            self.initialize_plugins()
        utils.setup_privileges()
        time.sleep(0.3)
        print("All plugins refreshed.")
        utils.echo(self.mumble.channels[self.mumble.users.myself['channel_id']],
                   "JJ Mumble Bot has refreshed all plugins.")
        logging.info("JJ Mumble Bot has refreshed all plugins.")

    def join_server(self):
        self.mumble.start()
        self.mumble.is_ready()
        self.bot_status = "Online"
        self.mumble.users.myself.comment(
            "This is JJMumbleBot [%s].<br>%s<br>" % (self.cfg_inst['Bot_Information']['BotVersion'], self.cfg_inst['Bot_Information']['KnownBugs']))
        self.mumble.set_bandwidth(192000)
        self.mumble.channels.find_by_name(self.cfg_inst['Connection_Settings']['DefaultChannel']).move_in()
        self.mumble.users.myself.mute()
        self.mumble.channels[self.mumble.users.myself['channel_id']].send_text_message("JJMumbleBot is Online.")
        print("\n\nJJMumbleBot is %s\n\n" % self.status())

    def status(self):
        return self.bot_status

    def message_received(self, text):
        message = text.message.strip()
        command = None
        user = self.mumble.users[text.actor]
        if "<img" in message:
            print("Message Received: [%s -> Image Data]" % user['name'])
        else:
            print("Message Received: [%s -> %s]" % (user['name'], message))

        if message[0] == "!":
            logging.info("Command Received: [%s -> %s]" % (user['name'], message))
            self.live_plugin_check()

            all_messages = message[1:].split()
            if len(all_messages) > 0:
                command = all_messages[0]
            else:
                return

            if command == "refresh":
                if utils.privileges_check(self.mumble.users[text.actor]) == pv.Privileges.ADMIN:
                    self.refresh_plugins()
                    return
                else:
                    print("User [%s] must be an admin to use this command." % (self.mumble.users[text.actor]['name']))
                    logging.warning("User [%s] tried to enter an admin-only command." % (self.mumble.users[text.actor]['name']))
                return

            elif command == "exit" or command == "quit":
                if utils.privileges_check(self.mumble.users[text.actor]) == pv.Privileges.ADMIN:
                    print("Stopping all threads...")
                    self.exit()
                    logging.info("JJ Mumble Bot is being shut down.")
                    return
                else:
                    print("User [%s] must be an admin to use this command." % (self.mumble.users[text.actor]['name']))
                    logging.warning("User [%s] tried to enter an admin-only command." % (self.mumble.users[text.actor]['name']))
                return

            elif command == "status":
                utils.echo(self.mumble.channels[self.mumble.users.myself['channel_id']],
                           "JJMumbleBot is %s." % self.status())
                return

            elif command == "system_test":
                if utils.privileges_check(self.mumble.users[text.actor]) == pv.Privileges.ADMIN:
                    self.plugin_callback_test()
                    logging.info("A system self-test was run.")
                    return
                else:
                    print("User [%s] must be an admin to use this command." % (self.mumble.users[text.actor]['name']))
                    logging.warning("User [%s] tried to enter an admin-only command." % (self.mumble.users[text.actor]['name']))
                return

            for plugin in self.bot_plugins.values():
                plugin.process_command(self.mumble, text)

    def exit(self):
        utils.echo(self.mumble.channels[self.mumble.users.myself['channel_id']],
                   "JJMumbleBot was manually disconnected.")
        for plugin in self.bot_plugins.values():
            plugin.quit()
        utils.clear_directory(utils.get_temporary_media_dir())
        utils.clear_directory(utils.get_temporary_img_dir())
        print("Cleared temporary directories.")
        self.exit_flag = True
        
    def loop(self):
        while not self.exit_flag:
            time.sleep(0.1)
