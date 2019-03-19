from templates.plugin_template import PluginBase
import utils


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> %s General Help Commands <font color='red'>#####</font></b><br> \
                All commands can be run by typing it in the chat or privately messaging JJMumbleBot.<br>\
                <b>!help</b>: Displays this general help screen.<br>\
                <b>!bot_help</b>: Displays the bot_commands plugin help screen.<br>\
                <b>!youtube_help/!yt_help</b>: Displays the youtube plugin help screen.<br>\
                <b>!sound_board_help/!sb_help</b>: Displays the sound_board plugin help screen.<br>\
                <b>!images_help/!img_help</b>: Displays the images plugin help screen.<br>\
                <b>!uptime_help</b> Displays the uptime plugin help screen." % utils.get_bot_name()

    bot_plugins = {}

    def __init__(self, bot_plugins):
        print("Help Plugin Initialized.")
        super().__init__()
        self.bot_plugins = bot_plugins

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "help":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       self.help())
            print("Displayed general help screen in the channel.")
            return
        elif command == "bot_help":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       self.bot_plugins.get('bot_commands').help())
            print("Displayed bot commands plugin help screen in the channel.")
            return
        elif command == "sound_board_help" or command == "sb_help":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       self.bot_plugins.get('sound_board').help())
            print("Displayed sound_board plugin help screen in the channel.")
            return
        elif command == "youtube_help" or command == "yt_help":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       self.bot_plugins.get('youtube').help())
            print("Displayed youtube plugin help screen in the channel.")
            return
        elif command == "images_help" or command == "img_help":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       self.bot_plugins.get('images').help())
            print("Displayed images plugin help screen in the channel.")
            return
        elif command == "uptime_help":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       self.bot_plugins.get('uptime').help())
            print("Displayed uptime plugin help screen in the channel.")
            return

    @staticmethod
    def plugin_test():
        print("Help Plugin self-test callback.")

    def quit(self):
        print("Exiting Help Plugin")

    def help(self):
        return self.help_data
