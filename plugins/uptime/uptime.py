import time
from templates.plugin_template import PluginBase
from helpers.global_access import debug_print, reg_print
from helpers.global_access import GlobalMods as GM
import privileges as pv
import utils


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
                        <b>!uptime</b>: Returns the bot uptime."
    plugin_version = "1.8.0"
    priv_path = "uptime/uptime_privileges.csv"
    
    start_seconds = 0
    seconds = 0
    minutes = 0
    hours = 0
    days = 0

    def __init__(self):
        debug_print("Uptime Plugin Initialized.")
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
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            # utils.echo(mumble.channels[mumble.users.myself['channel_id']],
            #           self.check_time())
            GM.gui.quick_gui(
                self.check_time(),
                text_type='header',
                box_align='left')
            return

    def plugin_test(self):
        debug_print("Uptime Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Uptime Plugin...")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
