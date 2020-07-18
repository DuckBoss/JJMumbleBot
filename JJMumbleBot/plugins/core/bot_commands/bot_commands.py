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

    def cmd_echo(self, data):
        to_echo = data.message.strip().split(' ', 1)[1]
        GS.gui_service.quick_gui(to_echo, text_type='header', box_align='left', ignore_whisper=True)
        dprint(f"Echo:[{to_echo}]", origin=L_COMMAND)
        log(INFO, f"Echo:[{to_echo}]", origin=L_COMMAND)

    def cmd_msg(self, data):
        split_data = data.message.strip().split(' ', 2)
        send_to = split_data[1]
        message_to_send = split_data[2]

        GS.gui_service.quick_gui(message_to_send, text_type='header', box_align='left',
                                 user=send_to,
                                 ignore_whisper=True)
        dprint(f"Msg:[{send_to}]->[{message_to_send}]", origin=L_COMMAND)
        log(INFO, f"Msg:[{send_to}]->[{message_to_send}]", origin=L_COMMAND)

    def cmd_log(self, data):
        to_log = data.message.strip().split(' ', 1)[1]
        dprint(f"Manually Logged: [{to_log}]", origin=L_LOGGING)
        log(INFO, f'Manually Logged: [{to_log}]', origin=L_LOGGING)

    def cmd_showplugins(self, data):
        cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>All Plugins:</font>"
        for i, plugin in enumerate(GS.bot_plugins.keys()):
            cur_text += f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{plugin}]"
        GS.gui_service.quick_gui(
            cur_text,
            text_type='header',
            box_align='left',
            text_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name']
        )

    def cmd_move(self, data):
        data_actor = GS.mumble_inst.users[data.actor]['name']
        channel_name = data.message.strip().split(' ', 1)[1]
        if channel_name == "default" or channel_name == "Default":
            channel_name = rutils.get_default_channel()
        channel_search = rutils.get_channel(channel_name)
        if channel_search is None:
            return
        channel_search.move_in()
        GS.gui_service.quick_gui(
            f"{rutils.get_bot_name()} was moved by {data_actor}",
            text_type='header', box_align='left', ignore_whisper=True)
        dprint(f"Moved to channel: {channel_name} by {data_actor}", origin=L_COMMAND)
        log(INFO, f"Moved to channel: {channel_name} by {data_actor}", origin=L_COMMAND)

    def cmd_make(self, data):
        data_actor = GS.mumble_inst.users[data.actor]['name']
        channel_name = data.message.strip().split(' ', 1)[1]
        rutils.make_channel(rutils.get_my_channel(), channel_name)
        dprint(f"Made a channel: {channel_name} by {data_actor}", origin=L_COMMAND)
        log(INFO, f"Made a channel: {channel_name} by {data_actor}", origin=L_COMMAND)

    def cmd_leave(self, data):
        rutils.leave_channel()
        dprint(f"Returned to default channel.", origin=L_COMMAND)
        log(INFO, "Returned to default channel.", origin=L_COMMAND)

    def cmd_remove(self, data):
        rutils.remove_channel()
        dprint(f"Removed current channel.", origin=L_COMMAND)
        log(INFO, "Removed current channel.", origin=L_COMMAND)

    def cmd_joinme(self, data):
        data_actor = GS.mumble_inst.users[data.actor]
        GS.gui_service.quick_gui(f"Joining user: {data_actor['name']}", text_type='header',
                                 box_align='left', ignore_whisper=True)

        GS.mumble_inst.channels[data_actor['channel_id']].move_in()
        log(INFO, f"Joined user: {data_actor['name']}", origin=L_COMMAND)

    def cmd_joinuser(self, data):
        try:
            to_join = data.message.strip().split(' ', 1)[1]
            all_users = rutils.get_all_users()
            for user_id in rutils.get_all_users():
                if all_users[user_id]['name'] == to_join:
                    GS.gui_service.quick_gui(f"Joining user: {all_users[user_id]['name']}", text_type='header',
                                             box_align='left', ignore_whisper=True)
                    GS.mumble_inst.channels[all_users[user_id]['channel_id']].move_in()
                    log(INFO, f"Joined user: {all_users[user_id]['name']}", origin=L_COMMAND)
        except IndexError:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}joinuser 'username'")
            GS.gui_service.quick_gui(
                f"Incorrect format! Format: {rutils.get_command_token()}joinuser 'username'",
                text_type='header',
                box_align='left', user=GS.mumble_inst.users[data.actor]['name'],
                ignore_whisper=True)

    def cmd_showprivileges(self, data):
        GS.gui_service.quick_gui(f"{privileges.get_all_privileges()}", text_type='header', box_align='left',
                                 text_align='left', user=GS.mumble_inst.users[data.actor]['name'],
                                 ignore_whisper=True)
        log(INFO, f"Displayed user privileges to: {GS.mumble_inst.users[data.actor]['name']}", origin=L_COMMAND)

    def cmd_setprivileges(self, data):
        data_actor = GS.mumble_inst.users[data.actor]
        try:
            username = data.message.strip().split()[1]
            level = int(data.message.strip().split()[2])
            result = privileges.set_privileges(username, level, data_actor)
            if result:
                GS.gui_service.quick_gui(f"User: {username} privileges have been modified.", text_type='header',
                                         box_align='left', user=data_actor['name'],
                                         ignore_whisper=True)
                log(INFO, f"Modified user privileges for: {username}", origin=L_USER_PRIV)
        except IndexError:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}setprivileges 'username' 'level'")
            GS.gui_service.quick_gui(f"Incorrect format! Format: {rutils.get_command_token()}setprivileges 'username' 'level'",
                                     text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)

    def cmd_addprivileges(self, data):
        data_actor = GS.mumble_inst.users[data.actor]
        try:
            username = data.message.strip().split()[1]
            level = int(data.message.strip().split()[2])
            result = privileges.add_to_privileges(username, level)
            if result:
                GS.gui_service.quick_gui(f"Added a new user: {username} to the user privileges.",
                                         text_type='header',
                                         box_align='left',
                                         user=data_actor['name'],
                                         ignore_whisper=True)
                log(INFO, f"Added a new user: {username} to the user privileges.", origin=L_USER_PRIV)
        except IndexError:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}addprivileges 'username' 'level'")
            GS.gui_service.quick_gui(f"Incorrect format! Format: {rutils.get_command_token()}addprivileges 'username' 'level'",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'],
                                     ignore_whisper=True)

    def cmd_showblacklist(self, data):
        GS.gui_service.quick_gui(privileges.get_blacklist(), text_type='header',
                                 box_align='left',
                                 text_align='left',
                                 user=GS.mumble_inst.users[data.actor]['name'],
                                 ignore_whisper=True
                                 )

    def cmd_blacklistuser(self, data):
        try:
            all_data = data.message.strip().split()
            reason = "No reason provided."
            if len(all_data) > 2:
                reason = all_data[2]
            result = privileges.add_to_blacklist(all_data[1])
            if result:
                GS.gui_service.quick_gui(f"User: {all_data[1]} added to the blacklist.<br>Reason: {reason}",
                                         text_type='header',
                                         box_align='left',
                                         text_align='left',
                                         user=GS.mumble_inst.users[data.actor]['name'],
                                         ignore_whisper=True
                                         )
                log(INFO, f"Blacklisted user: {all_data[1]} <br>Reason: {reason}", origin=L_USER_PRIV)
        except IndexError:
            rprint(f"Incorrect format! Format: {rutils.get_command_token()}blacklistuser 'username'")
            GS.gui_service.quick_gui(f"Incorrect format! Format: {rutils.get_command_token()}blacklistuser 'username'",
                                     text_type='header',
                                     box_align='left',
                                     user=GS.mumble_inst.users[data.actor]['name'],
                                     ignore_whisper=True)

    def cmd_whitelistuser(self, data):
        try:
            all_data = data.message.strip().split()
            result = privileges.remove_from_blacklist(all_data[1])
            if result:
                GS.gui_service.quick_gui(f"User: {all_data[1]} removed from the blacklist.",
                                         text_type='header',
                                         box_align='left',
                                         user=GS.mumble_inst.users[data.actor]['name'],
                                         ignore_whisper=True
                                         )
                log(INFO, f"User: {all_data[1]} removed from the blacklist.", origin=L_USER_PRIV)
        except IndexError:
            GS.gui_service.quick_gui("Command format: !whitelist username",
                                     text_type='header',
                                     box_align='left',
                                     user=GS.mumble_inst.users[data.actor]['name'],
                                     ignore_whisper=True
                                     )
