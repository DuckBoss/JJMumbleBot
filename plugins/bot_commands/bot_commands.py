import utils
from templates.plugin_template import PluginBase
import privileges as pv
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print, reg_print


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Bot_Commands Plugin Help <font color='red'>#####</font></b><br> \
            All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
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
            <b>!about</b>: Displays the bots about screen.<br>\
            <b>!spam_test: Spams 10 test messages in the channel. This is an admin-only command.<br>"
    plugin_version = "5.3.0"
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
            utils.echo(utils.get_my_channel(mumble), parameter)
            GM.logger.info("Echo:[%s]" % parameter)
            return

        elif command == "log":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            debug_print("Manually Logged: [%s]" % message_parse[1])
            GM.logger.info("Manually Logged: [%s]" % message_parse[1])
            return

        elif command == "spam_test":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            for i in range(10):
                utils.echo(utils.get_my_channel(mumble), "This is a spam_test message...")
                GM.logger.info("A spam_test was conducted by: %s." % mumble.users[text.actor]['name'])
            return

        elif command == "msg":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            utils.msg(mumble, all_messages[1], message[1:].split(' ', 2)[2])
            GM.logger.info("Msg:[%s]->[%s]" % (all_messages[1], message[1:].split(' ', 2)[2]))
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
                utils.echo(channel_search,
                           "%s was moved by %s" % (utils.get_bot_name(), mumble.users[text.actor]['name']))
                GM.logger.info("Moved to channel: %s by %s" % (channel_name, mumble.users[text.actor]['name']))
            return

        elif command == "make":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            parameter = message_parse[1]
            channel_name = parameter
            utils.make_channel(mumble, mumble.channels[mumble.users.myself['channel_id']], channel_name)
            GM.logger.info("Made a channel: %s by %s" % (channel_name, mumble.users[text.actor]['name']))
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
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "Joining user: %s" % mumble.users[text.actor]['name'])
            mumble.channels[mumble.users[text.actor]['channel_id']].move_in()
            GM.logger.info("Joined user: %s" % mumble.users[text.actor]['name'])
            return

        elif command == "privileges":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "%s" % pv.get_all_privileges())
            return

        elif command == "setprivileges":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                username = all_messages[1]
                level = int(all_messages[2])
                result = pv.set_privileges(username, level, mumble.users[text.actor])
                if result:
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "User: %s privileges have been modified." % username)
                    GM.logger.info("Modified user privileges for: %s" % username)
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
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "Added a new user: %s to the user privileges." % username)
                    GM.logger.info("Added a new user: %s to the user privileges." % username)
            except Exception:
                reg_print("Incorrect format! Format: !addprivileges 'username' 'level'")
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Incorrect format! Format: !addprivileges 'username' 'level'")
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
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "<br>User: %s added to the blacklist.<br>Reason: %s" % (parameter, reason))
                    GM.logger.info("<br>Blacklisted user: %s <br>Reason: %s" % (parameter, reason))
            except IndexError:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           pv.get_blacklist())
            return

        elif command == "whitelist":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                parameter = message_parse[1]
                result = pv.remove_from_blacklist(parameter)
                if result:
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "User: %s removed from the blacklist." % parameter)
                    GM.logger.info("<br>User: %s removed from the blacklist." % parameter)
            except IndexError:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Command format: !whitelist username")
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
