from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.resources.strings import *


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        import os
        import json
        raw_file = os.path.basename(__file__)
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{raw_file}')
        self.plugin_cmds = json.loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.priv_path = f'plugins/core/{raw_file.split(".")[0]}/privileges.csv'
        self.help_path = f'plugins/core/{raw_file.split(".")[0]}/help.html'
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]

        if command == "echo":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = message_parse[1]
            GS.gui_service.quick_gui(parameter, text_type='header', box_align='left', ignore_whisper=True)
            GS.log_service.info(f"Echo:[{parameter}]")
            return

        elif command == "msg":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            GS.gui_service.quick_gui(message[1:].split(' ', 2)[2], text_type='header', box_align='left',
                                     user=all_messages[1],
                                     ignore_whisper=True)
            GS.log_service.info(f"Msg:[{all_messages[1]}]->[{message[1:].split(' ', 2)[2]}]")
            return

        elif command == "log":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            dprint(f"Manually Logged: [{message_parse[1]}]")
            GS.log_service.info(f'Manually Logged: [{message_parse[1]}]')
            return

        elif command == "move":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = message_parse[1]
            channel_name = parameter
            if channel_name == "default" or channel_name == "Default":
                channel_name = rutils.get_default_channel()
            channel_search = rutils.get_channel(channel_name)
            if channel_search is None:
                return
            else:
                channel_search.move_in()
                GS.gui_service.quick_gui(
                    f"{rutils.get_bot_name()} was moved by {GS.mumble_inst.users[text.actor]['name']}",
                    text_type='header', box_align='left', ignore_whisper=True)
                GS.log_service.info(f"Moved to channel: {channel_name} by {GS.mumble_inst.users[text.actor]['name']}")
            return

        elif command == "make":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = message_parse[1]
            channel_name = parameter
            rutils.make_channel(rutils.get_my_channel(), channel_name)
            GS.log_service.info(f"Made a channel: {channel_name} by {GS.mumble_inst.users[text.actor]['name']}")
            return

        elif command == "leave":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            rutils.leave_channel()
            GS.log_service.info("Returned to default channel.")
            return

        elif command == "remove":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            rutils.remove_channel()
            GS.log_service.info("Removed current channel.")
            return

        elif command == "joinme":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            GS.gui_service.quick_gui(f"Joining user: {GS.mumble_inst.users[text.actor]['name']}", text_type='header',
                                     box_align='left', ignore_whisper=True)

            GS.mumble_inst.channels[GS.mumble_inst.users[text.actor]['channel_id']].move_in()
            GS.log_service.info(f"Joined user: {GS.mumble_inst.users[text.actor]['name']}")
            return

        elif command == "privileges":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            GS.gui_service.quick_gui(f"{privileges.get_all_privileges()}", text_type='header', box_align='left',
                                     text_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                     ignore_whisper=True)
            return

        elif command == "setprivileges":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                username = all_messages[1]
                level = int(all_messages[2])
                result = privileges.set_privileges(username, level, GS.mumble_inst.users[text.actor])
                if result:
                    GS.gui_service.quick_gui(f"User: {username} privileges have been modified.", text_type='header',
                                             box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True)
                    GS.log_service.info(f"Modified user privileges for: {username}")
            except Exception:
                rprint("Incorrect format! Format: !setprivileges 'username' 'level'")
                GS.gui_service.quick_gui("Incorrect format! Format: !setprivileges 'username' 'level'",
                                         text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            return

        elif command == "addprivileges":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                username = all_messages[1]
                level = int(all_messages[2])
                result = privileges.add_to_privileges(username, level)
                if result:
                    GS.gui_service.quick_gui(f"Added a new user: {username} to the user privileges.",
                                             text_type='header',
                                             box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True)
                    GS.log_service.info(f"Added a new user: {username} to the user privileges.")
            except Exception:
                rprint("Incorrect format! Format: !addprivileges 'username' 'level'")
                GS.gui_service.quick_gui("Incorrect format! Format: !addprivileges 'username' 'level'",
                                         text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            return

        elif command == "blacklist":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = all_messages[1]
                reason = "No reason provided."
                if len(message[1:].split()) >= 3:
                    reason = message[1:].split(' ', 2)[2]
                result = privileges.add_to_blacklist(parameter, GS.mumble_inst.users[text.actor])
                if result:
                    GS.gui_service.quick_gui(f"User: {parameter} added to the blacklist.<br>Reason: {reason}",
                                             text_type='header',
                                             box_align='left', text_align='left')
                    GS.log_service.info(f"Blacklisted user: {parameter} <br>Reason: {reason}")
            except IndexError:
                GS.gui_service.quick_gui(privileges.get_blacklist(), text_type='header',
                                         box_align='left', text_align='left')
            return

        elif command == "whitelist":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]
                result = privileges.remove_from_blacklist(parameter)
                if result:
                    GS.gui_service.quick_gui(f"User: {parameter} removed from the blacklist.", text_type='header',
                                             box_align='left')
                    GS.log_service.info(f"User: {parameter} removed from the blacklist.")
            except IndexError:
                GS.gui_service.quick_gui("Command format: !whitelist username", text_type='header',
                                         box_align='left')
                return
            return

    def quit(self):
        dprint("Exiting Bot_Commands Plugin...")

    def get_metadata(self):
        return self.metadata
