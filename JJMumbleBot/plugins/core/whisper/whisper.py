from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.lib.helpers import runtime_helper
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *


class Plugin(PluginBase):
    def get_metadata(self):
        return self.metadata

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
        command = message_parse[0]

        if command == "getwhisper":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if runtime_helper.whisper_target is None:
                GS.gui_service.quick_gui("There is no whisper target set", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            if runtime_helper.whisper_target["type"] == 0:
                ch = GS.mumble_inst.channels[runtime_helper.whisper_target['id']]['name']
                GS.gui_service.quick_gui(f"Current whisper channel: {ch}", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            elif runtime_helper.whisper_target["type"] == 1:
                us = ""
                for user in GS.mumble_inst.users:
                    if GS.mumble_inst.users[user]['session'] == runtime_helper.whisper_target['id']:
                        us = GS.mumble_inst.users[user]['name']
                GS.gui_service.quick_gui(f"Current whisper user: {us}", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            elif runtime_helper.whisper_target["type"] == 2:
                users = ""
                counter = 0
                for i, user in enumerate(GS.mumble_inst.users):
                    if GS.mumble_inst.users[user]['session'] in runtime_helper.whisper_target['id']:
                        users += f"<br>[{counter}] - {GS.mumble_inst.users[user]['name']}"
                        counter += 1
                GS.gui_service.quick_gui(f"Current whisper users: {users}", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return

        elif command == "setwhisperuser":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]
                if parameter == GS.cfg[C_CONNECTION_SETTINGS][P_USER_ID]:
                    GS.log_service.info("I can't set the whisper target to myself!")
                    GS.gui_service.quick_gui("I can't set the whisper target to myself!", text_type='header',
                                             box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True)
                    return
                rutils.set_whisper_user(parameter)

                GS.gui_service.quick_gui(f"Set whisper to User: {parameter}", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                GS.log_service.info(f"Set whisper to User: {parameter}.")
            except IndexError:
                GS.gui_service.quick_gui("Invalid whisper command!<br>Command format: !setwhisperuser username",
                                         text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            return

        elif command == "removewhisperuser":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                username = message_parse[1]
                if runtime_helper.whisper_target is not None:
                    if not isinstance(runtime_helper.whisper_target['id'], list):
                        GS.gui_service.quick_gui("<br>The current whisper mode is set to single user/channel."
                                                 "<br>You can only remove a user from a multi-user whisper mode."
                                                 "<br>Did you mean to use the 'clearwhisper' command?",
                                                 text_type='header',
                                                 box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                                 ignore_whisper=True)
                        return
                else:
                    return

                user_id = None
                for user in GS.mumble_inst.users:
                    if GS.mumble_inst.users[user]['name'] == username:
                        user_id = GS.mumble_inst.users[user]['session']
                if user_id is not None:
                    if user_id in runtime_helper.whisper_target['id']:
                        runtime_helper.whisper_target['id'].remove(user_id)
                    else:
                        GS.gui_service.quick_gui(f"Could not find user: {username} in the whisper targets!",
                                                 text_type='header',
                                                 box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                                 ignore_whisper=True)
                        return
                else:
                    GS.gui_service.quick_gui(f"Could not find user: {username} in the whisper targets!",
                                             text_type='header',
                                             box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True)
                    return
                if len(runtime_helper.whisper_target['id']) < 1:
                    rutils.clear_whisper()
                else:
                    rutils.set_whisper_multi_user(runtime_helper.whisper_target['id'])

                GS.gui_service.quick_gui(f"Removed user: {username} from the whisper targets!", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                GS.log_service.info(f"Removed user: {username} from the whisper targets!")
            except IndexError:
                GS.gui_service.quick_gui("Invalid whisper command!<br>Command format: !removewhisperuser username",
                                         text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            return

        elif command == "addwhisperuser":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                username = message_parse[1]
                if username == GS.cfg[C_CONNECTION_SETTINGS][P_USER_ID]:
                    GS.log_service.info("I can't add myself to the whisper targets!")
                    GS.gui_service.quick_gui("I can't add myself to the whisper targets!", text_type='header',
                                             box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True)
                    return
                if runtime_helper.whisper_target is not None:
                    if not isinstance(runtime_helper.whisper_target['id'], list):
                        GS.gui_service.quick_gui(
                            "<br>The current whisper mode is set to single user.<br>Use the 'setwhisperusers' command for multi-user whispers.",
                            text_type='header',
                            box_align='left', user=GS.mumble_inst.users[text.actor]['name'], ignore_whisper=True)
                        return
                else:
                    return
                for user in GS.mumble_inst.users:
                    if GS.mumble_inst.users[user]['name'] == username:
                        if GS.mumble_inst.users[user]['session'] in runtime_helper.whisper_target['id']:
                            GS.gui_service.quick_gui(
                                "<br>This user is already one of the whisper targets!",
                                text_type='header',
                                box_align='left', user=GS.mumble_inst.users[text.actor]['name'], ignore_whisper=True)
                            return

                runtime_helper.whisper_target['id'].append(username)
                rutils.set_whisper_multi_user(runtime_helper.whisper_target['id'])

                GS.gui_service.quick_gui(f"Added new user: {username} to the whisper targets!", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                GS.log_service.info(f"Added new user: {username} to the whisper targets!")
            except IndexError:
                GS.gui_service.quick_gui("Invalid whisper command!<br>Command format: !addwhisperuser username",
                                         text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            return

        elif command == "setwhisperusers":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]

                users_list = [user.strip() for user in parameter.split(',') if
                              not user.strip() == GS.cfg[C_CONNECTION_SETTINGS][P_USER_ID]]
                if len(users_list) < 2:
                    GS.gui_service.quick_gui("Use the 'setwhisperuser' command for a single user!", text_type='header',
                                             box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                             ignore_whisper=True)
                    return

                rutils.set_whisper_multi_user(users_list)

                GS.gui_service.quick_gui(f"Added whisper to multiple users!", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                GS.log_service.info(f"Added whisper to multiple users!")
            except IndexError:
                GS.gui_service.quick_gui(
                    "Invalid whisper command!<br>Command format: !setwhisperusers username0,username1,...",
                    text_type='header',
                    box_align='left', user=GS.mumble_inst.users[text.actor]['name'], ignore_whisper=True)
                return
            return

        elif command == "setwhisperme":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = GS.mumble_inst.users[text.actor]['name']
            if parameter == GS.cfg[C_CONNECTION_SETTINGS][P_USER_ID]:
                GS.log_service.info("I can't set the whisper target to myself!")
                return

            rutils.set_whisper_user(parameter)

            GS.gui_service.quick_gui(f"Set whisper to user: {parameter}", text_type='header',
                                     box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                     ignore_whisper=True)
            GS.log_service.info(f"Set whisper to user: {parameter}.")
            return

        elif command == "setwhisperchannel":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]
                rutils.set_whisper_channel(parameter)

                GS.gui_service.quick_gui(f"Set whisper to channel: {parameter}", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                GS.log_service.info(f"Set whisper to channel: {parameter}.")
            except IndexError:
                GS.gui_service.quick_gui("Command format: !setwhisperchannel channel_name", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            return

        elif command == "clearwhisper":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            rutils.clear_whisper()
            if runtime_helper.whisper_target is None:
                GS.gui_service.quick_gui(f"Cleared current whisper", text_type='header',
                                         box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                         ignore_whisper=True)
                return
            GS.gui_service.quick_gui("Unable to remove current whisper!", text_type='header',
                                     box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                                     ignore_whisper=True)
            return

    def quit(self):
        dprint("Exiting Whisper Plugin...")
