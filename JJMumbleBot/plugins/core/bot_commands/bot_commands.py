from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.resources.strings import *


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def get_metadata(self):
        return self.metadata

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]

        if command == "echo":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            parameter = message_parse[1]
            GS.gui_service.quick_gui(parameter, text_type='header', box_align='left', ignore_whisper=True)
            dprint(f"Echo:[{parameter}]", origin=L_COMMAND)
            log(INFO, f"Echo:[{parameter}]", origin=L_COMMAND)

        elif command == "msg":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.gui_service.quick_gui(message[1:].split(' ', 2)[2], text_type='header', box_align='left',
                                     user=all_messages[1],
                                     ignore_whisper=True)
            dprint(f"Msg:[{all_messages[1]}]->[{message[1:].split(' ', 2)[2]}]", origin=L_COMMAND)
            log(INFO, f"Msg:[{all_messages[1]}]->[{message[1:].split(' ', 2)[2]}]", origin=L_COMMAND)

        elif command == "log":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            dprint(f"Manually Logged: [{message_parse[1]}]", origin=L_LOGGING)
            log(INFO, f'Manually Logged: [{message_parse[1]}]', origin=L_LOGGING)

        elif command == "plugins":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>All Plugins:</font>"
            for i, plugin in enumerate(GS.bot_plugins.keys()):
                cur_text += f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{plugin}]"
            GS.gui_service.quick_gui(
                cur_text,
                text_type='header',
                box_align='left',
                text_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[text.actor]['name']
            )

        elif command == "duckaudio":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            rutils.toggle_ducking()
            GS.gui_service.quick_gui(
                f"{'Enabled' if rutils.can_duck() else 'Disabled'} audio volume ducking.",
                text_type='header',
                box_align='left')
            log(INFO, f"The bot audio ducking was {'enabled' if rutils.can_duck() else 'disabled'}.", origin=L_COMMAND)

        elif command == "duckvolume":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                GS.gui_service.quick_gui(
                    f"Current bot ducking volume: {rutils.get_ducking_volume()}",
                    text_type='header',
                    box_align='left')
                return
            if vol > 1 or vol < 0:
                GS.gui_service.quick_gui(
                    "Invalid Volume Input: [0-1]",
                    text_type='header',
                    box_align='left')
                return

            rutils.set_duck_volume(vol)
            GS.gui_service.quick_gui(
                f"Set volume to {vol}",
                text_type='header',
                box_align='left')
            log(INFO, f"The bot audio ducking volume was changed to {vol}.", origin=L_COMMAND)

        elif command == "volume":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                GS.gui_service.quick_gui(
                    f"Current bot volume: {rutils.get_volume()}",
                    text_type='header',
                    box_align='left')
                return
            if vol > 1 or vol < 0:
                GS.gui_service.quick_gui(
                    "Invalid Volume Input: [0-1]",
                    text_type='header',
                    box_align='left')
                return
            if rutils.is_ducking():
                rutils.set_last_volume(vol)
            else:
                rutils.set_volume(vol, auto=False)
            GS.gui_service.quick_gui(
                f"Set volume to {vol}",
                text_type='header',
                box_align='left')
            log(INFO, f"The bot audio volume was changed to {vol}.", origin=L_COMMAND)

        elif command == "move":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            parameter = message_parse[1]
            channel_name = parameter
            if channel_name == "default" or channel_name == "Default":
                channel_name = rutils.get_default_channel()
            channel_search = rutils.get_channel(channel_name)
            if channel_search is None:
                return
            channel_search.move_in()
            GS.gui_service.quick_gui(
                f"{rutils.get_bot_name()} was moved by {GS.mumble_inst.users[text.actor]['name']}",
                text_type='header', box_align='left', ignore_whisper=True)
            dprint(f"Moved to channel: {channel_name} by {GS.mumble_inst.users[text.actor]['name']}", origin=L_COMMAND)
            log(INFO, f"Moved to channel: {channel_name} by {GS.mumble_inst.users[text.actor]['name']}", origin=L_COMMAND)

        elif command == "make":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            parameter = message_parse[1]
            channel_name = parameter
            rutils.make_channel(rutils.get_my_channel(), channel_name)
            dprint(f"Made a channel: {channel_name} by {GS.mumble_inst.users[text.actor]['name']}", origin=L_COMMAND)
            log(INFO, f"Made a channel: {channel_name} by {GS.mumble_inst.users[text.actor]['name']}", origin=L_COMMAND)

        elif command == "leave":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            rutils.leave_channel()
            dprint(f"Returned to default channel.", origin=L_COMMAND)
            log(INFO, "Returned to default channel.", origin=L_COMMAND)

        elif command == "remove":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            rutils.remove_channel()
            dprint(f"Removed current channel.", origin=L_COMMAND)
            log(INFO, "Removed current channel.", origin=L_COMMAND)

        elif command == "joinme":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.gui_service.quick_gui(f"Joining user: {GS.mumble_inst.users[text.actor]['name']}", text_type='header',
                                     box_align='left', ignore_whisper=True)

            GS.mumble_inst.channels[GS.mumble_inst.users[text.actor]['channel_id']].move_in()
            log(INFO, f"Joined user: {GS.mumble_inst.users[text.actor]['name']}", origin=L_COMMAND)

        elif command == "privileges":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.gui_service.quick_gui(f"{privileges.get_all_privileges()}", text_type='header', box_align='left',
                                     text_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                     ignore_whisper=True)

        elif command == "setprivileges":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                username = all_messages[1]
                level = int(all_messages[2])
                result = privileges.set_privileges(username, level, GS.mumble_inst.users[text.actor])
                if result:
                    GS.gui_service.quick_gui(f"User: {username} privileges have been modified.", text_type='header',
                                             box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True)
                    log(INFO, f"Modified user privileges for: {username}", origin=L_USER_PRIV)
            except Exception:
                rprint("Incorrect format! Format: !setprivileges 'username' 'level'")
                GS.gui_service.quick_gui("Incorrect format! Format: !setprivileges 'username' 'level'",
                                         text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)

        elif command == "addprivileges":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                username = all_messages[1]
                level = int(all_messages[2])
                result = privileges.add_to_privileges(username, level)
                if result:
                    GS.gui_service.quick_gui(f"Added a new user: {username} to the user privileges.",
                                             text_type='header',
                                             box_align='left',
                                             user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True)
                    log(INFO, f"Added a new user: {username} to the user privileges.", origin=L_USER_PRIV)
            except Exception:
                rprint("Incorrect format! Format: !addprivileges 'username' 'level'")
                GS.gui_service.quick_gui("Incorrect format! Format: !addprivileges 'username' 'level'",
                                         text_type='header',
                                         box_align='left',
                                         user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)

        elif command == "blacklist":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                parameter = all_messages[1]
                reason = "No reason provided."
                if len(message[1:].split()) >= 3:
                    reason = message[1:].split(' ', 2)[2]
                result = privileges.add_to_blacklist(parameter)
                if result:
                    GS.gui_service.quick_gui(f"User: {parameter} added to the blacklist.<br>Reason: {reason}",
                                             text_type='header',
                                             box_align='left',
                                             text_align='left',
                                             user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True
                                             )
                    log(INFO, f"Blacklisted user: {parameter} <br>Reason: {reason}", origin=L_USER_PRIV)
            except IndexError:
                GS.gui_service.quick_gui(privileges.get_blacklist(), text_type='header',
                                         box_align='left',
                                         text_align='left',
                                         user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True
                                         )

        elif command == "whitelist":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                parameter = message_parse[1]
                result = privileges.remove_from_blacklist(parameter)
                if result:
                    GS.gui_service.quick_gui(f"User: {parameter} removed from the blacklist.",
                                             text_type='header',
                                             box_align='left',
                                             user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True
                                             )
                    log(INFO, f"User: {parameter} removed from the blacklist.", origin=L_USER_PRIV)
            except IndexError:
                GS.gui_service.quick_gui("Command format: !whitelist username",
                                         text_type='header',
                                         box_align='left',
                                         user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True
                                         )
