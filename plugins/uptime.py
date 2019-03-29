import time
from templates.plugin_template import PluginBase
import utils


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Uptime Plugin Help <font color='red'>#####</font></b><br> \
                        All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
                        <b>!uptime</b>: Returns the bot uptime."
    plugin_version = "1.0.0"
    
    start_seconds = 0
    seconds = 0
    minutes = 0
    hours = 0
    days = 0

    def __init__(self):
        print("Uptime Plugin Initialized.")
        super().__init__()
        self.start_seconds = time.time()

    def check_time(self):
        self.seconds = time.time() - self.start_seconds
        while self.seconds >= 60:
            self.minutes += 1
            self.seconds -= 60
        while self.minutes >= 60:
            self.hours += 1
            self.minutes -= 60
        while self.hours >= 24:
            self.days += 1
            self.hours -= 24
        return "Uptime: {%dd : %dh : %dm : %ds}" % (int(self.days), int(self.hours), int(self.minutes), int(self.seconds))

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "uptime":
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       self.check_time())
            return

    def plugin_test(self):
        print("Uptime Plugin self-test callback.")

    def quit(self):
        print("Exiting Uptime Plugin...")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version
