from templates.plugin_template import PluginBase
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print
import utils
import privileges as pv


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
                        <b>!setwhisperuser 'username'</b>: Sets the whisper target to the given user<br>\
                        <b>!setwhisperusers 'username1,username2,...'</b>: Sets the whisper target to multiple users.<br>\
                        <b>!addwhisperuser 'username'</b>: Adds the user to the whisper targets.<br>\
                        <b>!setwhisperme</b>: Sets the whisper target to the command sender.<br>\
                        <b>!setwhisperchannel 'channelname'</b>: Sets the whisper target to the given channel.<br>\
                        <b>!clearwhisper</b>: Clears any previously set whisper target.<br>\
                        <b>!removewhisperuser 'username'</b>: Removes a specific user from the whisper targets.<br>\
                        <b>!getwhisper</b>: Displays the current whisper target."
    plugin_version = "2.2.0"
    priv_path = "whisper/whisper_privileges.csv"
    
    def __init__(self):
        debug_print("Whisper Plugin Initialized.")
        super().__init__()

    def process_command(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "getwhisper":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if GM.whisper_target is None:
                GM.gui.quick_gui("There is no whisper target set", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            if GM.whisper_target["type"] == 0:
                ch = GM.mumble.channels[GM.whisper_target['id']]['name']
                GM.gui.quick_gui(f"Current whisper channel: {ch}", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            elif GM.whisper_target["type"] == 1:
                us = ""
                for user in GM.mumble.users:
                    if GM.mumble.users[user]['session'] == GM.whisper_target['id']:
                        us = GM.mumble.users[user]['name']
                GM.gui.quick_gui(f"Current whisper user: {us}", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            elif GM.whisper_target["type"] == 2:
                users = ""
                counter = 0
                for i, user in enumerate(GM.mumble.users):
                    if GM.mumble.users[user]['session'] in GM.whisper_target['id']:
                        users += f"<br>[{counter}] - {GM.mumble.users[user]['name']}"
                        counter += 1
                GM.gui.quick_gui(f"Current whisper users: {users}", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return

        elif command == "setwhisperuser":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]
                if parameter == GM.cfg['Connection_Settings']['UserID']:
                    GM.logger.info("I can't set the whisper target to myself!")
                    GM.gui.quick_gui("I can't set the whisper target to myself!", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                    return
                utils.set_whisper_user(parameter)

                GM.gui.quick_gui(f"Set whisper to User: {parameter}", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                GM.logger.info(f"Set whisper to User: {parameter}.")
            except IndexError:
                GM.gui.quick_gui("Invalid whisper command!<br>Command format: !setwhisperuser username", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            return

        elif command == "removewhisperuser":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                username = message_parse[1]
                if GM.whisper_target is not None:
                    if not isinstance(GM.whisper_target['id'], list):
                        GM.gui.quick_gui("<br>The current whisper mode is set to single user/channel."
                                         "<br>You can only remove a user from a multi-user whisper mode."
                                         "<br>Did you mean to use the 'clearwhisper' command?", text_type='header',
                                         box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                        return
                else:
                    return

                user_id = None
                for user in GM.mumble.users:
                    if GM.mumble.users[user]['name'] == username:
                        user_id = GM.mumble.users[user]['session']
                if user_id is not None:
                    if user_id in GM.whisper_target['id']:
                        GM.whisper_target['id'].remove(user_id)
                    else:
                        GM.gui.quick_gui(f"Could not find user: {username} in the whisper targets!", text_type='header',
                                         box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                        return
                else:
                    GM.gui.quick_gui(f"Could not find user: {username} in the whisper targets!", text_type='header',
                                     box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                    return
                if len(GM.whisper_target['id']) < 1:
                    utils.clear_whisper()
                else:
                    utils.set_whisper_multi_user(GM.whisper_target['id'])

                GM.gui.quick_gui(f"Removed user: {username} from the whisper targets!", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                GM.logger.info(f"Removed user: {username} from the whisper targets!")
            except IndexError:
                GM.gui.quick_gui("Invalid whisper command!<br>Command format: !removewhisperuser username", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            return

        elif command == "addwhisperuser":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                username = message_parse[1]
                if username == GM.cfg['Connection_Settings']['UserID']:
                    GM.logger.info("I can't add myself to the whisper targets!")
                    GM.gui.quick_gui("I can't add myself to the whisper targets!", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                    return
                if GM.whisper_target is not None:
                    if not isinstance(GM.whisper_target['id'], list):
                        GM.gui.quick_gui("<br>The current whisper mode is set to single user.<br>Use the 'setwhisperusers' command for multi-user whispers.", text_type='header',
                                         box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                        return
                else:
                    return
                for user in GM.mumble.users:
                    if GM.mumble.users[user]['name'] == username:
                        if GM.mumble.users[user]['session'] in GM.whisper_target['id']:
                            GM.gui.quick_gui(
                                "<br>This user is already one of the whisper targets!",
                                text_type='header',
                                box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                            return

                GM.whisper_target['id'].append(username)
                utils.set_whisper_multi_user(GM.whisper_target['id'])

                GM.gui.quick_gui(f"Added new user: {username} to the whisper targets!", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                GM.logger.info(f"Added new user: {username} to the whisper targets!")
            except IndexError:
                GM.gui.quick_gui("Invalid whisper command!<br>Command format: !addwhisperuser username", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            return

        elif command == "setwhisperusers":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]

                users_list = [user.strip() for user in parameter.split(',') if not user.strip() == GM.cfg['Connection_Settings']['UserID']]
                if len(users_list) < 2:
                    GM.gui.quick_gui("Use the 'setwhisperuser' command for a single user!", text_type='header',
                                     box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                    return

                utils.set_whisper_multi_user(users_list)

                GM.gui.quick_gui(f"Added whisper to multiple users!", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                GM.logger.info(f"Added whisper to multiple users!")
            except IndexError:
                GM.gui.quick_gui("Invalid whisper command!<br>Command format: !setwhisperusers username0,username1,...", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            return

        elif command == "setwhisperme":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = GM.mumble.users[text.actor]['name']
            if parameter == GM.cfg['Connection_Settings']['UserID']:
                GM.logger.info("I can't set the whisper target to myself!")
                return

            utils.set_whisper_user(parameter)

            GM.gui.quick_gui(f"Set whisper to user: {parameter}", text_type='header',
                             box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
            GM.logger.info(f"Set whisper to user: {parameter}.")
            return

        elif command == "setwhisperchannel":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]
                utils.set_whisper_channel(parameter)

                GM.gui.quick_gui(f"Set whisper to channel: {parameter}", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                GM.logger.info(f"Set whisper to channel: {parameter}.")
            except IndexError:
                GM.gui.quick_gui("Command format: !setwhisperchannel channel_name", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            return

        elif command == "clearwhisper":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            utils.clear_whisper()
            if GM.whisper_target is None:
                GM.gui.quick_gui(f"Cleared current whisper", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            GM.gui.quick_gui("Unable to remove current whisper!", text_type='header',
                             box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
            return


    def plugin_test(self):
        debug_print("Whisper Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Whisper Plugin...")

    def help(self):
        return self.help_data

    def is_audio_plugin(self):
        return False

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path

