import pymumble_py3 as pymumble
from JJMumbleBot.lib.utils.web_utils import RemoteTextMessage
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
from JJMumbleBot.lib.helpers import runtime_helper
from JJMumbleBot.lib.utils.logging_utils import log, initialize_logging
from JJMumbleBot.lib.pgui import PseudoGUI
from JJMumbleBot.lib.mumble_data import MumbleData
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.helpers.queue_handler import QueueHandler
from JJMumbleBot.lib.cmd_history import CMDQueue
from JJMumbleBot.lib.database import init_database
from JJMumbleBot.lib.utils import dir_utils, runtime_utils
from JJMumbleBot.lib.utils.print_utils import rprint
from JJMumbleBot.lib.command import Command
from JJMumbleBot.lib import aliases
from JJMumbleBot.lib import execute_cmd
from JJMumbleBot.lib import errors
from JJMumbleBot.lib.vlc.audio_interface import create_vlc_single_instance
from JJMumbleBot.lib.vlc.vlc_api import VLCInterface, VLCStatus
from time import sleep
from datetime import datetime
from copy import deepcopy


class BotService:
    def __init__(self):
        # Initialize bot services.
        global_settings.bot_service = self
        # Initialize user settings.
        BotServiceHelper.initialize_settings()
        # Initialize logging services.
        initialize_logging()
        # Check and classify system arguments.
        import JJMumbleBot.core.cla_classifier as cla
        cla.classify()

        log(INFO, "######### Initializing JJMumbleBot #########", origin=L_STARTUP)
        rprint("######### Initializing JJMumbleBot #########", origin=L_STARTUP)
        # Initialize up-time tracking.
        runtime_helper.start_time = datetime.now()
        # Set maximum multi-command limit.
        runtime_settings.multi_cmd_limit = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_MULTI_LIM])
        # Initialize command queue limit.
        global_settings.cmd_queue = QueueHandler(runtime_settings.cmd_hist_lim)
        # Initialize command history tracking.
        global_settings.cmd_history = CMDQueue(runtime_settings.cmd_hist_lim)
        log(INFO, "######### Initializing Internal Database #########", origin=L_DATABASE)
        rprint("######### Initializing Internal Database #########", origin=L_DATABASE)
        # Back up bot database.
        db_backup = BotServiceHelper.backup_database()
        log(INFO, f"Created internal database backup @ {db_backup}", origin=L_DATABASE)
        rprint(f"Created internal database backup @ {db_backup}", origin=L_DATABASE)
        # Initialize bot database.
        global_settings.mumble_db = init_database()
        log(INFO, "######### Initialized Internal Database #########", origin=L_DATABASE)
        rprint("######### Initialized Internal Database #########", origin=L_DATABASE)
        # Initialize major directories.
        dir_utils.make_directory(global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR])
        dir_utils.make_directory(f'{global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/internal/images')
        dir_utils.make_directory(f'{global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/internal/audio')
        log(INFO, "Initialized Temporary Directories.", origin=L_STARTUP)
        rprint("Initialized Temporary Directories.", origin=L_STARTUP)
        # Initialize PGUI system.
        global_settings.gui_service = PseudoGUI()
        log(INFO, "Initialized PGUI.", origin=L_STARTUP)
        rprint("Initialized PGUI.", origin=L_STARTUP)
        # Initialize VLC interface.
        # global_settings.vlc_interface = VLCInterface("192.168.1.200", "8080", "", global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PASS])
        # global_settings.vlc_status = VLCStatus("192.168.1.200", "8080", "", global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PASS])
        # create_vlc_single_instance()
        # Initialize plugins.
        if global_settings.safe_mode:
            BotServiceHelper.initialize_plugins_safe()
            runtime_settings.tick_rate = 0.2
            log(INFO, "Initialized plugins with safe mode.", origin=L_STARTUP)
            rprint("Initialized plugins with safe mode.", origin=L_STARTUP)
        else:
            BotServiceHelper.initialize_plugins()
            log(INFO, "Initialized all plugins.", origin=L_STARTUP)
            rprint("Initialized all plugins.", origin=L_STARTUP)
        log(INFO, "######### Initializing Mumble Client #########", origin=L_STARTUP)
        rprint("######### Initializing Mumble Client #########", origin=L_STARTUP)
        # Retrieve mumble client data from configs.
        mumble_login_data = BotServiceHelper.retrieve_mumble_data()
        BotService.initialize_mumble(mumble_login_data)
        log(INFO, "######### Initialized Mumble Client #########", origin=L_STARTUP)
        rprint("######### Initialized Mumble Client #########", origin=L_STARTUP)
        # Initialize web interface
        if global_settings.cfg.getboolean(C_WEB_SETTINGS, P_WEB_ENABLE) and global_settings.safe_mode is False:
            log(INFO, "######### Initializing Web Interface #########", origin=L_WEB_INTERFACE)
            rprint("######### Initializing Web Interface #########", origin=L_WEB_INTERFACE)
            from JJMumbleBot.web import web_helper
            web_helper.initialize_web()
            log(INFO, "######### Initialized Web Interface #########", origin=L_WEB_INTERFACE)
            rprint("######### Initialized Web Interface #########", origin=L_WEB_INTERFACE)
        # Start runtime loop.
        BotService.loop()

    @staticmethod
    def initialize_mumble(md: MumbleData):
        global_settings.mumble_inst = pymumble.Mumble(md.ip_address, port=md.port, user=md.user_id,
                                                      password=md.password, certfile=md.certificate, stereo=md.stereo)
        global_settings.mumble_inst.callbacks.set_callback('text_received', BotService.message_received)
        global_settings.mumble_inst.callbacks.set_callback('connected', BotService.on_connected)
        global_settings.mumble_inst.set_codec_profile('audio')
        global_settings.mumble_inst.start()
        global_settings.mumble_inst.is_ready()
        if global_settings.cfg.getboolean(C_CONNECTION_SETTINGS, P_SELF_REGISTER):
            global_settings.mumble_inst.users.myself.register()
        global_settings.mumble_inst.users.myself.comment(
            f'{runtime_utils.get_comment()}<br>[{META_NAME}({META_VERSION})] - {runtime_utils.get_bot_name()}<br>{runtime_utils.get_about()}')
        runtime_utils.mute()
        runtime_utils.get_channel(global_settings.cfg[C_CONNECTION_SETTINGS][P_CHANNEL_DEF]).move_in()

    @staticmethod
    def message_received(text, remote_cmd=False):
        all_commands = runtime_utils.parse_message(text)
        if all_commands is None:
            return
        # Iterate through all commands provided and generate commands.
        for i, item in enumerate(all_commands):
            # Generate command with parameters
            if not remote_cmd:
                new_text = deepcopy(text)
            else:
                new_text = RemoteTextMessage(channel_id=global_settings.mumble_inst.users.myself['channel_id'],
                                             session=global_settings.mumble_inst.users.myself['session'],
                                             message=text.message,
                                             actor=global_settings.mumble_inst.users.myself['session'])
            new_text.message = item
            try:
                new_command = Command(item[1:].split()[0], new_text)
            except IndexError:
                continue
            all_aliases = aliases.get_all_aliases()
            all_alias_names = [x[0] for x in all_aliases]
            if len(all_aliases) != 0:
                if new_command.command in all_alias_names:
                    alias_item_index = all_alias_names.index(new_command.command)
                    alias_commands = [msg.strip() for msg in all_aliases[alias_item_index][1].split('|')]
                    if len(alias_commands) > runtime_settings.multi_cmd_limit:
                        rprint(
                            f"The multi-command limit was reached! "
                            f"The multi-command limit is {runtime_settings.multi_cmd_limit} "
                            f"commands per line.", origin=L_COMMAND)
                        log(WARNING,
                            f"The multi-command limit was reached! "
                            f"The multi-command limit is {runtime_settings.multi_cmd_limit} "
                            f"commands per line.", origin=L_COMMAND)
                        return
                    for x, sub_item in enumerate(alias_commands):
                        if not remote_cmd:
                            sub_text = deepcopy(text)
                        else:
                            sub_text = RemoteTextMessage(
                                channel_id=global_settings.mumble_inst.users.myself['channel_id'],
                                session=global_settings.mumble_inst.users.myself['session'],
                                message=text.message,
                                actor=global_settings.mumble_inst.users.myself['session'])
                        if len(item[1:].split()) > 1:
                            sub_text.message = f"{sub_item} {item[1:].split(' ', 1)[1]}"
                        else:
                            sub_text.message = sub_item
                        try:
                            sub_command = Command(sub_item[1:].split()[0], sub_text)
                        except IndexError:
                            continue
                        global_settings.cmd_queue.insert(sub_command)
                else:
                    # Insert command into the command queue
                    global_settings.cmd_queue.insert(new_command)
            else:
                global_settings.cmd_queue.insert(new_command)

        # Process commands if the queue is not empty
        while not global_settings.cmd_queue.is_empty():
            # Process commands in the queue
            BotService.process_command_queue(global_settings.cmd_queue.pop())
            sleep(runtime_settings.tick_rate)

    @staticmethod
    def process_command_queue(com):
        execute_cmd.execute_command(com)

    @staticmethod
    def on_connected():
        log(INFO, f"{runtime_utils.get_bot_name()} is Online.", origin=L_STARTUP)

    @staticmethod
    def loop():
        while not global_settings.exit_flag:
            sleep(runtime_settings.tick_rate)
        BotService.stop()

    @staticmethod
    def stop():
        import sys
        global_settings.mumble_inst.stop()
        sys.exit(0)
