import utils
from templates.plugin_template import PluginBase
import privileges as pv
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print, reg_print


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
            <b>!echo 'message/image'</b>: Echoes a message/image in the chat.<br>\
            <b>!log 'message'</b>: Manually logs a message by an administrator.<br>\
            <b>!make 'channel_name'</b>: Creates a channel with the given name.<br>\
            <b>!move 'channel_name'</b>: Moves to an existing channel with the given name.<br>\
            <b>!move default/Default</b>: Moves the bot to the default channel stated in the config.ini file.<br>\
            <b>!joinme</b>: Moves to the users channel.<br>\
            <b>!msg 'username' 'message'</b>: Anonymously private messages a user from the bot.<br>\
            <b>!leave</b>: Moves the bot to the default channel.<br>\
            <b>!exit/!quit</b>: Initializes the bot exit procedure.<br>\
            <b>!privileges</b>: Displays the full user list with privilege levels.<br>\
            <b>!setprivileges 'username' 'level'</b>: Sets a user's privilege level.<br>\
            <b>!addprivileges 'username' 'level'</b>: Adds a new user to the user privilege list.<br>\
            <b>!blacklist</b>: Displays the current list of users in the blacklist.<br>\
            <b>!blacklist 'username'</b>: Blacklists specific users from using certain plugin commands.<br>\
            <b>!whitelist 'username'</b>: Removes an existing user from the blacklist.<br>\
            <b>!setwhisperuser 'username'</b>: Sets the whisper target to the given user<br>\
            <b>!setwhisperusers 'username1,username2,...'</b>: Sets the whisper target to multiple users.<br>\
            <b>!addwhisperuser 'username'</b>: Adds the user to the whisper targets.<br>\
            <b>!setwhisperme</b>: Sets the whisper target to the command sender.<br>\
            <b>!setwhisperchannel 'channelname'</b>: Sets the whisper target to the given channel.<br>\
            <b>!clearwhisper</b>: Clears any previously set whisper target.<br>\
            <b>!removewhisperuser 'username'</b>: Removes a specific user from the whisper targets.<br>\
            <b>!getwhisper</b>: Displays the current whisper target.<br>\
            <b>!version</b>: Displays the bot version.<br>\
            <b>!status</b>: Displays the bots current status.<br>\
            <b>!refresh</b>: Refreshes all plugins.<br>\
            <b>!reboot/!restart</b>: Completely stops the bot and restarts it.<br>\
            <b>!about</b>: Displays the bots about screen.<br>\
            <b>!uptime</b>: Displays the amount of time the bot has been online.<br>\
            <b>!spam_test</b>: Spams 10 test messages in the channel. This is an admin-only command.<br>"
    plugin_version = "2.2.0"
    priv_path = "bot_commands/bot_commands_privileges.csv"

    def __init__(self):
        debug_print("Bot_Commands Plugin Initialized.")
        super().__init__()

    def process_command(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]

        if command == "echo":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = message_parse[1]
            GM.gui.quick_gui(parameter, text_type='header', box_align='left', ignore_whisper=True)
            GM.logger.info(f"Echo:[{parameter}]")
            return

        elif command == "log":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            debug_print(f"Manually Logged: [{message_parse[1]}]")
            GM.logger.info(f"Manually Logged: [{message_parse[1]}]")
            return

        elif command == "spam_test":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            for i in range(10):
                GM.gui.quick_gui("This is a spam test message...", text_type='header', box_align='left', ignore_whisper=True)
            GM.logger.info(f"A spam_test was conducted by: {GM.mumble.users[text.actor]['name']}.")
            return

        elif command == "msg":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.quick_gui(message[1:].split(' ', 2)[2], text_type='header', box_align='left', user=all_messages[1], ignore_whisper=True)
            GM.logger.info(f"Msg:[{all_messages[1]}]->[{message[1:].split(' ', 2)[2]}]")
            return

        elif command == "move":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = message_parse[1]
            channel_name = parameter
            if channel_name == "default" or channel_name == "Default":
                channel_name = utils.get_default_channel()
            channel_search = utils.get_channel(channel_name)
            if channel_search is None:
                return
            else:
                channel_search.move_in()
                GM.gui.quick_gui(f"{utils.get_bot_name()} was moved by {GM.mumble.users[text.actor]['name']}", text_type='header', box_align='left', ignore_whisper=True)
                GM.logger.info(f"Moved to channel: {channel_name} by {GM.mumble.users[text.actor]['name']}")
            return

        elif command == "make":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = message_parse[1]
            channel_name = parameter
            utils.make_channel(utils.get_my_channel(), channel_name)
            GM.logger.info(f"Made a channel: {channel_name} by {GM.mumble.users[text.actor]['name']}")
            return

        elif command == "leave":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            utils.leave()
            GM.logger.info("Returned to default channel.")
            return

        elif command == "joinme":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.quick_gui(f"Joining user: {GM.mumble.users[text.actor]['name']}", text_type='header', box_align='left', ignore_whisper=True)

            GM.mumble.channels[GM.mumble.users[text.actor]['channel_id']].move_in()
            GM.logger.info(f"Joined user: {GM.mumble.users[text.actor]['name']}")
            return

        elif command == "privileges":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            GM.gui.quick_gui(f"{pv.get_all_privileges()}", text_type='header', box_align='left', text_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
            return

        elif command == "setprivileges":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                username = all_messages[1]
                level = int(all_messages[2])
                result = pv.set_privileges(username, level, GM.mumble.users[text.actor])
                if result:
                    GM.gui.quick_gui(f"User: {username} privileges have been modified.", text_type='header', box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                    GM.logger.info(f"Modified user privileges for: {username}")
            except Exception:
                reg_print("Incorrect format! Format: !setprivileges 'username' 'level'")
                GM.gui.quick_gui("Incorrect format! Format: !setprivileges 'username' 'level'", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            return

        elif command == "addprivileges":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                username = all_messages[1]
                level = int(all_messages[2])
                result = pv.add_to_privileges(username, level)
                if result:
                    GM.gui.quick_gui(f"Added a new user: {username} to the user privileges.", text_type='header',
                                     box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                    GM.logger.info(f"Added a new user: {username} to the user privileges.")
            except Exception:
                reg_print("Incorrect format! Format: !addprivileges 'username' 'level'")
                GM.gui.quick_gui("Incorrect format! Format: !addprivileges 'username' 'level'", text_type='header',
                                 box_align='left', user=GM.mumble.users[text.actor]['name'], ignore_whisper=True)
                return
            return

        elif command == "blacklist":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = all_messages[1]
                reason = "No reason provided."
                print(len(message[1:].split()))
                if len(message[1:].split()) >= 3:
                    reason = message[1:].split(' ', 2)[2]
                result = pv.add_to_blacklist(parameter, GM.mumble.users[text.actor])
                if result:
                    GM.gui.quick_gui(f"User: {parameter} added to the blacklist.<br>Reason: {reason}", text_type='header',
                                     box_align='left', text_align='left')
                    GM.logger.info(f"Blacklisted user: {parameter} <br>Reason: {reason}")
            except IndexError:
                GM.gui.quick_gui(pv.get_blacklist(), text_type='header',
                                 box_align='left', text_align='left')
            return

        elif command == "whitelist":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]
                result = pv.remove_from_blacklist(parameter)
                if result:
                    GM.gui.quick_gui(f"User: {parameter} removed from the blacklist.", text_type='header',
                                     box_align='left')
                    GM.logger.info(f"User: {parameter} removed from the blacklist.")
            except IndexError:
                GM.gui.quick_gui("Command format: !whitelist username", text_type='header',
                                 box_align='left')
                return
            return

        elif command == "getwhisper":
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
        debug_print("Bot_Commands Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Bot_Commands Plugin...")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version

    def is_audio_plugin(self):
        return False

    def get_priv_path(self):
        return self.priv_path
