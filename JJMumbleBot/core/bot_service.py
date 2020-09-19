import pymumble_py3 as pymumble
from pymumble_py3.constants import PYMUMBLE_CLBK_USERCREATED, PYMUMBLE_CLBK_CONNECTED, PYMUMBLE_CLBK_SOUNDRECEIVED, \
    PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, PYMUMBLE_CLBK_DISCONNECTED, PYMUMBLE_CLBK_CHANNELUPDATED, \
    PYMUMBLE_CLBK_CHANNELREMOVED, PYMUMBLE_CLBK_CHANNELCREATED, PYMUMBLE_CLBK_USERREMOVED, PYMUMBLE_CLBK_USERUPDATED
from JJMumbleBot.core.callback_service import CallbackService
from JJMumbleBot.lib.utils.web_utils import RemoteTextMessage
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
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
from JJMumbleBot.lib.audio.audio_api import AudioLibraryInterface
from time import sleep, time
import audioop
from datetime import datetime
from copy import deepcopy


class BotService:
    def __init__(self, serv_ip, serv_port, serv_pass):
        # Initialize bot services.
        global_settings.bot_service = self
        global_settings.clbk_service = CallbackService()
        # Initialize user settings.
        BotServiceHelper.initialize_settings()
        # Initialize logging services.
        initialize_logging()

        log(INFO, "######### Initializing JJMumbleBot #########", origin=L_STARTUP)
        rprint("######### Initializing JJMumbleBot #########", origin=L_STARTUP)
        # Initialize up-time tracking.
        runtime_settings.start_time = datetime.now()
        # Set maximum multi-command limit.
        runtime_settings.multi_cmd_limit = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_MULTI_LIM])
        # Initialize command queue limit.
        global_settings.cmd_queue = QueueHandler([], maxlen=runtime_settings.cmd_queue_lim)
        # Initialize command history tracking.
        global_settings.cmd_history = CMDQueue(runtime_settings.cmd_hist_lim)
        log(INFO, "######### Initializing Internal Database #########", origin=L_DATABASE)
        rprint("######### Initializing Internal Database #########", origin=L_DATABASE)
        # Back up internal database.
        if global_settings.cfg.getboolean(C_MAIN_SETTINGS, P_DB_BACKUP, fallback=False):
            db_backup = BotServiceHelper.backup_database()
            if db_backup:
                log(INFO, f"Created internal database backup @ {db_backup}", origin=L_DATABASE)
                rprint(f"Created internal database backup @ {db_backup}", origin=L_DATABASE)
        # Initialize internal database.
        global_settings.mumble_db = init_database()
        log(INFO, "######### Initialized Internal Database #########", origin=L_DATABASE)
        rprint("######### Initialized Internal Database #########", origin=L_DATABASE)
        # Initialize major directories.
        if global_settings.cfg.get(C_MEDIA_SETTINGS, P_TEMP_MED_DIR, fallback=None):
            dir_utils.make_directory(global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR])
        else:
            dir_utils.make_directory(f'{dir_utils.get_main_dir()}/TemporaryMediaDirectory')
            global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR] = f'{dir_utils.get_main_dir()}/TemporaryMediaDirectory'
        if global_settings.cfg.get(C_MEDIA_SETTINGS, P_PERM_MEDIA_DIR, fallback=None):
            dir_utils.make_directory(global_settings.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR])
        else:
            dir_utils.make_directory(f'{dir_utils.get_main_dir()}/PermanentMediaDirectory')
            global_settings.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR] = f'{dir_utils.get_main_dir()}/PermanentMediaDirectory'
        if global_settings.cfg.get(C_MEDIA_SETTINGS, P_LOG_DIR, fallback=None):
            dir_utils.make_directory(global_settings.cfg[C_MEDIA_SETTINGS][P_LOG_DIR])
        else:
            dir_utils.make_directory(f'{dir_utils.get_main_dir()}/Logs')
            global_settings.cfg[C_MEDIA_SETTINGS][P_LOG_DIR] = f'{dir_utils.get_main_dir()}/Logs'
        dir_utils.make_directory(f'{global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/internal/images')
        dir_utils.make_directory(f'{global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/internal/audio')
        log(INFO, "######### Initialized Temporary Directories #########", origin=L_STARTUP)
        rprint("######### Initialized Temporary Directories #########", origin=L_STARTUP)
        # Initialize PGUI system.
        global_settings.gui_service = PseudoGUI()
        log(INFO, "######### Initialized PGUI #########", origin=L_STARTUP)
        rprint("######### Initialized PGUI #########", origin=L_STARTUP)
        # Initialize VLC interface.
        global_settings.aud_interface = AudioLibraryInterface()
        # Initialize plugins.
        if global_settings.safe_mode:
            BotServiceHelper.initialize_plugins_safe()
            runtime_settings.tick_rate = 0.2
            log(INFO, "Initialized plugins with safe mode.", origin=L_STARTUP)
            rprint("Initialized plugins with safe mode.", origin=L_STARTUP)
        else:
            BotServiceHelper.initialize_plugins()
        log(INFO, "######### Initializing Mumble Client #########", origin=L_STARTUP)
        rprint("######### Initializing Mumble Client #########", origin=L_STARTUP)
        # Retrieve mumble client data from configs.
        mumble_login_data = BotServiceHelper.retrieve_mumble_data(serv_ip, serv_port, serv_pass)
        self.initialize_mumble(mumble_login_data)
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

    def initialize_mumble(self, md: MumbleData):
        global_settings.mumble_inst = pymumble.Mumble(md.ip_address, port=md.port, user=md.user_id, reconnect=md.auto_reconnect,
                                                  password=md.password, certfile=md.certificate, stereo=md.stereo)
        # Callback - message_received
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED,
                                                           global_settings.clbk_service.message_received)
        global_settings.core_callbacks.append_to_callback(PYMUMBLE_CLBK_TEXTMESSAGERECEIVED, self.message_received)
        # Callback - sound_received
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_SOUNDRECEIVED,
                                                           global_settings.clbk_service.sound_received)
        global_settings.core_callbacks.append_to_callback(PYMUMBLE_CLBK_SOUNDRECEIVED, self.sound_received)
        # Callback - on_connected
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_CONNECTED,
                                                           global_settings.clbk_service.connected)
        global_settings.core_callbacks.append_to_callback(PYMUMBLE_CLBK_CONNECTED, self.on_connected)
        # Callback - disconnected
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_DISCONNECTED,
                                                           global_settings.clbk_service.disconnected)
        # Callback - user_created
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_USERCREATED,
                                                           global_settings.clbk_service.user_created)
        # Callback - user_updated
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_USERUPDATED,
                                                           global_settings.clbk_service.user_updated)
        # Callback - user_removed
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_USERREMOVED,
                                                           global_settings.clbk_service.user_removed)
        # Callback - channel_created
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_CHANNELCREATED,
                                                           global_settings.clbk_service.channel_created)
        # Callback - channel_removed
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_CHANNELREMOVED,
                                                           global_settings.clbk_service.channel_removed)
        # Callback - channel_updated
        global_settings.mumble_inst.callbacks.set_callback(PYMUMBLE_CLBK_CHANNELUPDATED,
                                                           global_settings.clbk_service.channel_updated)

        global_settings.mumble_inst.set_codec_profile('audio')
        global_settings.mumble_inst.set_receive_sound(True)
        global_settings.mumble_inst.start()
        global_settings.mumble_inst.is_ready()

        if global_settings.cfg.getboolean(C_CONNECTION_SETTINGS, P_SELF_REGISTER, fallback=False):
            global_settings.mumble_inst.users.myself.register()
        global_settings.mumble_inst.users.myself.comment(
            f'{runtime_utils.get_comment()}<br>[{META_NAME}({META_VERSION})] - {runtime_utils.get_bot_name()}<br>{runtime_utils.get_about()}')
        runtime_utils.mute()
        runtime_utils.get_channel(global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_CHANNEL]).move_in()

    def message_received(self, message):
        text = message[0]
        remote_cmd = message[1]
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
                        if len(item.split()) > 1:
                            sub_text.message = f"{sub_item} {item.split(' ', 1)[1]}"
                        else:
                            sub_text.message = sub_item
                        try:
                            com_parse = sub_item.split()[0]
                            if com_parse[0] != '(' and com_parse[-1] != ')':
                                return
                            sub_command = Command(com_parse[1:][:-1], sub_text)
                        except IndexError:
                            continue
                        global_settings.cmd_queue.insert_item(sub_command)
                else:
                    # Insert command into the command queue
                    global_settings.cmd_queue.insert_item(new_command)
            else:
                global_settings.cmd_queue.insert_item(new_command)

        # Process commands if the queue is not empty
        while not global_settings.cmd_queue.is_empty():
            # Process commands in the queue
            BotService.process_command_queue(global_settings.cmd_queue.pop_item())
            sleep(runtime_settings.tick_rate)

    @staticmethod
    def process_command_queue(com):
        execute_cmd.execute_command(com)

    def on_connected(self):
        log(INFO, f"{runtime_utils.get_bot_name()} is Online.", origin=L_STARTUP)

    def sound_received(self, audio_data):
        user = audio_data[0]
        audio_chunk = audio_data[1]
        if audioop.rms(audio_chunk.pcm, 2) > global_settings.aud_interface.status['ducking_threshold'] and global_settings.aud_interface.status['duck_audio']:
            global_settings.aud_interface.audio_utilities.duck_volume()
            global_settings.aud_interface.status['duck_start'] = time()
            global_settings.aud_interface.status['duck_end'] = time() + global_settings.aud_interface.audio_utilities.get_ducking_delay()

    @staticmethod
    def loop():
        try:
            while not global_settings.exit_flag:
                if time() > global_settings.aud_interface.status['duck_end'] and global_settings.aud_interface.audio_utilities.is_ducking():
                    global_settings.aud_interface.audio_utilities.unduck_volume()
                sleep(runtime_settings.tick_rate)
            BotService.stop()
        except KeyboardInterrupt:
            rprint(f"{runtime_utils.get_bot_name()} was booted offline by a keyboard interrupt (ctrl-c).", origin=L_SHUTDOWN)
            log(INFO, f"{runtime_utils.get_bot_name()} was booted offline by a keyboard interrupt (ctrl-c).", origin=L_SHUTDOWN)
            runtime_utils.exit_bot()
            BotService.stop()

    @staticmethod
    def stop():
        import sys
        global_settings.mumble_inst.stop()
        sys.exit(0)
