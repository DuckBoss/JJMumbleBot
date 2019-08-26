from JJMumbleBot.lib.pymumble import pymumble_py3 as pymumble
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
from JJMumbleBot.lib.pgui import PseudoGUI
from JJMumbleBot.lib.mumble_data import MumbleData
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.helpers.queue_handler import QueueHandler
from JJMumbleBot.lib.cmd_history import CMDQueue
from JJMumbleBot.lib.enums import BotState
from JJMumbleBot.lib.utils import dir_utils, runtime_utils
from JJMumbleBot.lib.utils.print_utils import rprint
from JJMumbleBot.lib.command import Command
from JJMumbleBot.lib import aliases
from JJMumbleBot.lib import execute_cmd
from JJMumbleBot.lib.monitor import monitor_service
from time import time, sleep
import copy


class BotService:
    def __init__(self):
        # Initialize bot services.
        global_settings.bot_service = self
        # Initialize user settings.
        BotServiceHelper.initialize_settings()
        # Initialize logging services.
        BotServiceHelper.initialize_logging()
        BotServiceHelper.log(INFO, "###########################")
        BotServiceHelper.log(INFO, "Initializing JJMumbleBot...")
        # Initialize bot state.
        global_settings.status = BotState.OFFLINE
        # Initialize up-time tracking.
        global_settings.start_seconds = time()
        # Initialize command queue limit.
        global_settings.cmd_queue = QueueHandler(runtime_settings.cmd_hist_lim)
        # Initialize command history tracking.
        global_settings.cmd_history = CMDQueue(runtime_settings.cmd_hist_lim)
        # Initialize command aliases.
        aliases.setup_aliases()
        BotServiceHelper.log(INFO, "Initialized command aliases.")
        # Initialize major directories.
        dir_utils.make_directory(global_settings.cfg[C_MEDIA_DIR][P_TEMP_IMG_DIR])
        BotServiceHelper.log(INFO, "Initialized temporary directories.")
        dir_utils.make_directory(f'{global_settings.cfg[C_MEDIA_DIR][P_PERM_MEDIA_DIR]}/sound_board/')
        dir_utils.make_directory(f'{global_settings.cfg[C_MEDIA_DIR][P_PERM_MEDIA_DIR]}/images/')
        BotServiceHelper.log(INFO, "Initialized permanent directories.")
        # Initialize PGUI system.
        global_settings.gui_service = PseudoGUI()
        BotServiceHelper.log(INFO, "Initialized pseudo graphical user interface.")
        # Initialize plugins.
        if global_settings.safe_mode:
            BotServiceHelper.initialize_plugins_safe()
            runtime_settings.tick_rate = 0.2
            BotServiceHelper.log(INFO, "Initialized plugins with safe mode.")
        else:
            BotServiceHelper.initialize_plugins()
            BotServiceHelper.log(INFO, "Initialized all plugins.")
        # Retrieve mumble client data from configs.
        mumble_login_data = BotServiceHelper.retrieve_mumble_data()
        BotService.initialize_mumble(mumble_login_data)
        # Start monitor service thread.
        """
        if runtime_settings.use_web_interface:
            import threading
            from JJMumbleBot.lib.monitor import monitor_test
            global_settings.monitor_thr = threading.Thread(target=monitor_test.loop_monitor_check)
            global_settings.monitor_thr.daemon = True
            global_settings.monitor_thr.run()
        """
        # Initialize web service.
        if runtime_settings.use_web_interface:
            import threading
            from JJMumbleBot.lib.web.web_interface.web_service import start_server
            runtime_settings.web_ip = global_settings.cfg[C_WEB_INT][P_WEB_IP]
            runtime_settings.web_port = int(global_settings.cfg[C_WEB_INT][P_WEB_PORT])
            runtime_settings.web_thread = threading.Thread(target=start_server)
            runtime_settings.web_thread.daemon = True
            runtime_settings.web_thread.start()
        # Start runtime loop.
        BotService.loop()

    @staticmethod
    def initialize_mumble(md: MumbleData):
        global_settings.mumble_inst = pymumble.Mumble(md.ip_address, port=md.port, user=md.user_id,
                                                      password=md.password, certfile=md.certificate)
        global_settings.mumble_inst.callbacks.set_callback('text_received', BotService.message_received)
        global_settings.mumble_inst.callbacks.set_callback('connected', BotService.on_connected)
        global_settings.mumble_inst.set_codec_profile('audio')
        global_settings.mumble_inst.start()
        global_settings.mumble_inst.is_ready()
        global_settings.status = BotState.ONLINE

    @staticmethod
    def message_received(text):
        all_commands = runtime_utils.parse_message(text)
        if all_commands is None:
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
                if len(alias_commands) > runtime_settings.multi_cmd_limit:
                    rprint(
                        f"The multi-command limit was reached! The multi-command limit is {runtime_settings.multi_cmd_limit} commands per line.")
                    BotServiceHelper.log(WARNING,
                        f"The multi-command limit was reached! The multi-command limit is {runtime_settings.multi_cmd_limit} commands per line.")
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
                    global_settings.cmd_queue.insert(sub_command)
            else:
                # Insert command into the command queue
                global_settings.cmd_queue.insert(new_command)
        # Process commands if the queue is not empty
        while not global_settings.cmd_queue.is_empty():
            # Process commands in the queue
            BotService.process_command_queue(global_settings.cmd_queue.pop())
            sleep(runtime_settings.tick_rate)

    @staticmethod
    def process_command_queue(com):
        for plugin in global_settings.bot_plugins.values():
            execute_cmd.execute_command(plugin, com)

    @staticmethod
    def on_connected():
        BotServiceHelper.log(INFO, f"{runtime_utils.get_bot_name()} is online.")

    @staticmethod
    def loop():
        while not global_settings.exit_flag:
            monitor_service.loop_monitor_check()
            # print("updated monitor data")
            sleep(runtime_settings.tick_rate)
        BotService.stop()

    @staticmethod
    def stop():
        import sys
        sys.exit(0)

