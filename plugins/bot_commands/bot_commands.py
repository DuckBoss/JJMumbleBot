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
            <b>!version</b>: Displays the bot version.<br>\
            <b>!status</b>: Displays the bots current status.<br>\
            <b>!refresh</b>: Refreshes all plugins.<br>\
            <b>!reboot/!restart</b>: Completely stops the bot and restarts it.<br>\
            <b>!about</b>: Displays the bots about screen.<br>\
            <b>!spam_test</b>: Spams 10 test messages in the channel. This is an admin-only command.<br>"
    plugin_version = "1.8.1"
    priv_path = "bot_commands/bot_commands_privileges.csv"

    def __init__(self):
        debug_print("Bot_Commands Plugin Initialized.")
        super().__init__()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]

        if command == "echo":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            parameter = message_parse[1]
            GM.gui.quick_gui(parameter, text_type='header', box_align='left')
            GM.logger.info(f"Echo:[{parameter}]")
            return

        elif command == "log":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            debug_print(f"Manually Logged: [{message_parse[1]}]")
            GM.logger.info(f"Manually Logged: [{message_parse[1]}]")
            return

        elif command == "spam_test":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            for i in range(10):
                # utils.echo(utils.get_my_channel(mumble), "This is a spam_test message...")
                GM.gui.quick_gui("This is a spam test message...", text_type='header', box_align='left')
            GM.logger.info(f"A spam_test was conducted by: {mumble.users[text.actor]['name']}.")
            return

        elif command == "msg":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            # utils.msg(mumble, all_messages[1], message[1:].split(' ', 2)[2])
            GM.gui.quick_gui(message[1:].split(' ', 2)[2], text_type='header', box_align='left', user=all_messages[1])
            GM.logger.info(f"Msg:[{all_messages[1]}]->[{message[1:].split(' ', 2)[2]}]")
            return

        elif command == "move":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            parameter = message_parse[1]
            channel_name = parameter
            if channel_name == "default" or channel_name == "Default":
                channel_name = utils.get_default_channel()
            channel_search = utils.get_channel(mumble, channel_name)
            if channel_search is None:
                return
            else:
                channel_search.move_in()
                # utils.echo(channel_search,
                #           f"{utils.get_bot_name()} was moved by {mumble.users[text.actor]['name']}")
                GM.gui.quick_gui(f"{utils.get_bot_name()} was moved by {mumble.users[text.actor]['name']}", text_type='header', box_align='left')
                GM.logger.info(f"Moved to channel: {channel_name} by {mumble.users[text.actor]['name']}")
            return

        elif command == "make":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            parameter = message_parse[1]
            channel_name = parameter
            utils.make_channel(mumble, utils.get_my_channel(mumble), channel_name)
            GM.logger.info(f"Made a channel: {channel_name} by {mumble.users[text.actor]['name']}")
            return

        elif command == "leave":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            utils.leave(mumble)
            GM.logger.info("Returned to default channel.")
            return

        elif command == "joinme":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            # utils.echo(utils.get_my_channel(mumble),
            #           f"Joining user: {mumble.users[text.actor]['name']}")
            GM.gui.quick_gui(f"Joining user: {mumble.users[text.actor]['name']}", text_type='header', box_align='left')

            mumble.channels[mumble.users[text.actor]['channel_id']].move_in()
            GM.logger.info(f"Joined user: {mumble.users[text.actor]['name']}")
            return

        elif command == "privileges":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            # utils.echo(utils.get_my_channel(mumble),
            #            f"{pv.get_all_privileges()}")
            GM.gui.quick_gui(f"{pv.get_all_privileges()}", text_type='header', box_align='left', text_align='left')
            return

        elif command == "setprivileges":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                username = all_messages[1]
                level = int(all_messages[2])
                result = pv.set_privileges(username, level, mumble.users[text.actor])
                if result:
                    # utils.echo(utils.get_my_channel(mumble),
                    #           f"User: {username} privileges have been modified.")
                    GM.gui.quick_gui(f"User: {username} privileges have been modified.", text_type='header', box_align='left')
                    GM.logger.info(f"Modified user privileges for: {username}")
            except Exception:
                reg_print("Incorrect format! Format: !setprivileges 'username' 'level'")
                return
            return

        elif command == "addprivileges":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                username = all_messages[1]
                level = int(all_messages[2])
                result = pv.add_to_privileges(username, level)
                if result:
                    # utils.echo(utils.get_my_channel(mumble),
                    #           f"Added a new user: {username} to the user privileges.")
                    GM.gui.quick_gui(f"Added a new user: {username} to the user privileges.", text_type='header',
                                     box_align='left')
                    GM.logger.info(f"Added a new user: {username} to the user privileges.")
            except Exception:
                reg_print("Incorrect format! Format: !addprivileges 'username' 'level'")
                # utils.echo(utils.get_my_channel(mumble),
                #           "Incorrect format! Format: !addprivileges 'username' 'level'")
                GM.gui.quick_gui("Incorrect format! Format: !addprivileges 'username' 'level'", text_type='header',
                                 box_align='left')
                return
            return

        elif command == "blacklist":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                parameter = all_messages[1]
                reason = "No reason provided."
                print(len(message[1:].split()))
                if len(message[1:].split()) >= 3:
                    reason = message[1:].split(' ', 2)[2]
                result = pv.add_to_blacklist(parameter, mumble.users[text.actor])
                if result:
                    # utils.echo(utils.get_my_channel(mumble),
                    #           "<br>User: {parameter} added to the blacklist.<br>Reason: {reason}")
                    GM.gui.quick_gui(f"User: {parameter} added to the blacklist.<br>Reason: {reason}", text_type='header',
                                     box_align='left', text_align='left')
                    GM.logger.info(f"<br>Blacklisted user: {parameter} <br>Reason: {reason}")
            except IndexError:
                # utils.echo(utils.get_my_channel(mumble),
                #           pv.get_blacklist())
                GM.gui.quick_gui(pv.get_blacklist(), text_type='header',
                                 box_align='left', text_align='left')
            return

        elif command == "whitelist":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]
                result = pv.remove_from_blacklist(parameter)
                if result:
                    # utils.echo(utils.get_my_channel(mumble),
                    #           "User: {parameter} removed from the blacklist.")
                    GM.gui.quick_gui(f"User: {parameter} removed from the blacklist.", text_type='header',
                                     box_align='left')
                    GM.logger.info(f"<br>User: {parameter} removed from the blacklist.")
            except IndexError:
                # utils.echo(utils.get_my_channel(mumble),
                #           "Command format: !whitelist username")
                GM.gui.quick_gui("Command format: !whitelist username", text_type='header',
                                 box_align='left')
                return
            return

    @staticmethod
    def plugin_test():
        debug_print("Bot_Commands Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Bot_Commands Plugin...")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
