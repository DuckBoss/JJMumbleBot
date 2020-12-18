from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.plugins.core.whisper.resources.strings import *
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.settings import runtime_settings as rs
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.resources.strings import *


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        log(
            INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value
        )

    def quit(self):
        log(
            INFO,
            f"Exiting {self.plugin_name} plugin...",
            origin=L_SHUTDOWN,
            print_mode=PrintMode.REG_PRINT.value
        )

    def cmd_getwhisper(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        if rs.whisper_target is None:
            gs.gui_service.quick_gui("There is no whisper target set", text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
            return
        if rs.whisper_target["type"] == 0:
            ch = gs.mumble_inst.channels[rs.whisper_target['id']]['name']
            gs.gui_service.quick_gui(f"Current whisper channel: {ch}", text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
        elif rs.whisper_target["type"] == 1:
            us = ""
            for user in gs.mumble_inst.users:
                if gs.mumble_inst.users[user]['session'] == rs.whisper_target['id']:
                    us = gs.mumble_inst.users[user]['name']
            gs.gui_service.quick_gui(f"Current whisper user: {us}", text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
        elif rs.whisper_target["type"] == 2:
            users = ""
            counter = 0
            for i, user in enumerate(gs.mumble_inst.users):
                if gs.mumble_inst.users[user]['session'] in rs.whisper_target['id']:
                    users += f"<br>[{counter}] - {gs.mumble_inst.users[user]['name']}"
                    counter += 1
            gs.gui_service.quick_gui(f"Current whisper users: {users}", text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)

    def cmd_setwhisperuser(self, data):
        all_data = data.message.strip().split(' ', 1)
        data_actor = gs.mumble_inst.users[data.actor]
        try:
            parameter = all_data[1]
            if parameter == gs.cfg[C_CONNECTION_SETTINGS][P_USER_ID]:
                log(INFO, INFO_INVALID_WHISPER_CLIENT, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
                gs.gui_service.quick_gui(INFO_INVALID_WHISPER_CLIENT, text_type='header',
                                         box_align='left', user=data_actor['name'],
                                         ignore_whisper=True)
                return
            if rutils.set_whisper_user(parameter):
                gs.gui_service.quick_gui(f"Set whisper to User: {parameter}", text_type='header',
                                         box_align='left', user=data_actor['name'],
                                         ignore_whisper=True)
                log(INFO, f"Set whisper to User: {parameter}.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

            gs.gui_service.quick_gui(f"Could not find User: {parameter}", text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
        except IndexError:
            log(ERROR, INFO_INVALID_WHISPER_CLIENT,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                INFO_INVALID_WHISPER_CLIENT,
                text_type='header',
                box_align='left', user=data_actor['name'],
                ignore_whisper=True)
            return

    def cmd_removewhisperuser(self, data):
        all_data = data.message.strip().split(' ', 1)
        data_actor = gs.mumble_inst.users[data.actor]
        try:
            username = all_data[1]
            if rs.whisper_target is not None:
                if not isinstance(rs.whisper_target['id'], list):
                    gs.gui_service.quick_gui("<br>The current whisper mode is set to single user/channel."
                                             "<br>You can only remove a user from a multi-user whisper mode."
                                             "<br>Did you mean to use the 'clearwhisper' command?",
                                             text_type='header',
                                             box_align='left', user=data_actor['name'],
                                             ignore_whisper=True)
                    return
            else:
                return

            user_id = None
            for user in gs.mumble_inst.users:
                if gs.mumble_inst.users[user]['name'] == username:
                    user_id = gs.mumble_inst.users[user]['session']
            if user_id is not None:
                if user_id in rs.whisper_target['id']:
                    rs.whisper_target['id'].remove(user_id)
                else:
                    gs.gui_service.quick_gui(f"Could not find user: {username} in the whisper targets.",
                                             text_type='header',
                                             box_align='left', user=data_actor['name'],
                                             ignore_whisper=True)
                    return
            else:
                gs.gui_service.quick_gui(f"Could not find user: {username} in the whisper targets.",
                                         text_type='header',
                                         box_align='left', user=data_actor['name'],
                                         ignore_whisper=True)
                return
            if len(rs.whisper_target['id']) < 1:
                rutils.clear_whisper()
            else:
                rutils.set_whisper_multi_user(rs.whisper_target['id'])

            gs.gui_service.quick_gui(f"Removed user: {username} from the whisper targets.", text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
            log(INFO, f"Removed user: {username} from the whisper targets.", origin=L_COMMAND)
        except IndexError:
            log(ERROR, CMD_INVALID_REMOVE_WHISPER,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(CMD_INVALID_REMOVE_WHISPER,
                                     text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
            return

    def cmd_addwhisperuser(self, data):
        all_data = data.message.strip().split(' ', 1)
        data_actor = gs.mumble_inst.users[data.actor]
        try:
            username = all_data[1]
            if username == gs.cfg[C_CONNECTION_SETTINGS][P_USER_ID]:
                log(INFO, INFO_INVALID_WHISPER_CLIENT, origin=L_COMMAND)
                gs.gui_service.quick_gui(INFO_INVALID_WHISPER_CLIENT, text_type='header',
                                         box_align='left', user=data_actor['name'],
                                         ignore_whisper=True)
                return
            if rs.whisper_target is not None:
                if not isinstance(rs.whisper_target['id'], list):
                    gs.gui_service.quick_gui(
                        "The current whisper mode is set to single user.<br>Use the 'setwhisperusers' command for multi-user whispers.",
                        text_type='header',
                        box_align='left', user=data_actor['name'], ignore_whisper=True)
                    return
            else:
                return
            for user in gs.mumble_inst.users:
                if gs.mumble_inst.users[user]['name'] == username:
                    if gs.mumble_inst.users[user]['session'] in rs.whisper_target['id']:
                        gs.gui_service.quick_gui(
                            "This user is already one of the whisper targets!",
                            text_type='header',
                            box_align='left', user=data_actor['name'], ignore_whisper=True)
                        return

            rs.whisper_target['id'].append(username)
            rutils.set_whisper_multi_user(rs.whisper_target['id'])
            gs.gui_service.quick_gui(f"Added new user: {username} to the whisper targets!", text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
            log(INFO, f"Added new user: {username} to the whisper targets!", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        except IndexError:
            log(ERROR, CMD_INVALID_REMOVE_WHISPER,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                CMD_INVALID_ADD_WHISPER,
                text_type='header',
                box_align='left', user=data_actor['name'],
                ignore_whisper=True)
            return

    def cmd_setwhisperusers(self, data):
        all_data = data.message.strip().split(' ', 1)
        data_actor = gs.mumble_inst.users[data.actor]
        try:
            parameter = all_data[1]

            users_list = [user.strip() for user in parameter if
                          not user.strip() == gs.cfg[C_CONNECTION_SETTINGS][P_USER_ID]]
            if len(users_list) < 2:
                gs.gui_service.quick_gui("Use the 'setwhisperuser' command for a single user!", text_type='header',
                                         box_align='left', user=data_actor['name'],
                                         ignore_whisper=True)
                return

            rutils.set_whisper_multi_user(users_list)
            gs.gui_service.quick_gui(f"Added whisper to multiple users!", text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
            log(INFO, INFO_ADDED_MULTIPLE_WHISPER, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        except IndexError:
            log(ERROR, CMD_INVALID_SET_WHISPER_USERS,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                CMD_INVALID_SET_WHISPER_USERS,
                text_type='header',
                box_align='left', user=data_actor['name'], ignore_whisper=True)
            return

    def cmd_setwhisperme(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        if data_actor == gs.cfg[C_CONNECTION_SETTINGS][P_USER_ID]:
            log(ERROR, INFO_INVALID_WHISPER_CLIENT, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            return

        rutils.set_whisper_user(data_actor['name'])
        gs.gui_service.quick_gui(f"Set whisper to user: {data_actor['name']}", text_type='header',
                                 box_align='left', user=data_actor['name'],
                                 ignore_whisper=True)
        log(INFO, f"Set whisper to user: {data_actor['name']}.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_setwhisperchannel(self, data):
        all_data = data.message.strip().split(' ', 1)
        data_actor = gs.mumble_inst.users[data.actor]
        try:
            parameter = all_data[1]
            if rutils.set_whisper_channel(parameter):
                gs.gui_service.quick_gui(f"Set whisper to channel: {parameter}", text_type='header',
                                         box_align='left', user=data_actor['name'],
                                         ignore_whisper=True)
                log(INFO, f"Set whisper to channel: {parameter}.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            else:
                gs.gui_service.quick_gui(f"Could not find channel: {parameter}", text_type='header',
                                         box_align='left', user=data_actor['name'],
                                         ignore_whisper=True)
        except IndexError:
            log(ERROR, CMD_INVALID_WHISPER_CHANNEL, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(CMD_INVALID_WHISPER_CHANNEL,
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
            return

    def cmd_clearwhisper(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        rutils.clear_whisper()
        if rs.whisper_target is None:
            log(INFO, f"Cleared current whisper targets", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(f"Cleared current whisper", text_type='header',
                                     box_align='left', user=data_actor['name'],
                                     ignore_whisper=True)
            return
        log(INFO, f"Unable to remove current whisper targets", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui("Unable to remove current whisper!", text_type='header',
                                 box_align='left', user=data_actor['name'],
                                 ignore_whisper=True)
