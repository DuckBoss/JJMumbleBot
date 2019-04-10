from templates.plugin_template import PluginBase
from helpers.global_access import debug_print, reg_print
import utils
import privileges as pv
import os
import random


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Randomizer General Help Commands <font color='red'>#####</font></b><br> \
                All commands can be run by typing it in the chat or privately messaging JJMumbleBot.<br>\
                <b>!customroll 'number_of_dice' 'dice_faces'</b>: A custom dice roll with multiple dice and custom face counts.<br>\
                <b>!coinflip</b>: A coin flip 2-sided roll.<br>\
                <b>!d4roll</b>: A standard 4-sided dice roll.<br>\
                <b>!d6roll</b>: A standard 6-sided dice roll.<br>\
                <b>!d8roll</b>: A standard 8-sided dice roll.<br>\
                <b>!d10roll</b>: A standard 10-sided dice roll.<br>\
                <b>!d12roll</b> A standard 12-sided dice roll.<br>\
                <b>!d20roll</b> A standard 20-sided dice roll."
    plugin_version = "1.6.0"
    priv_path = "randomizer/randomizer_privileges.csv"

    def __init__(self):
        debug_print("Randomizer Plugin Initialized.")
        super().__init__()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "coinflip":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1,2)
            if result == 1:
                result = "Heads"
            else:
                result = "Tails"
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "<font color='cyan'>Coin Flip Result:</font> <font color='yellow'>%s</font>" % result)
            return
        elif command == "d4roll":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1,4)
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "<font color='cyan'>D4 Roll Result:</font> <font color='yellow'>%s</font>" % result)
            return
        elif command == "d6roll":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1,6)
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "<font color='cyan'>D6 Roll Result:</font> <font color='yellow'>%s</font>" % result)
            return
        elif command == "d8roll":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1,8)
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "<font color='cyan'>D8 Roll Result:</font> <font color='yellow'>%s</font>" % result)
            return
        elif command == "d10roll":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1,10)
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "<font color='cyan'>D10 Roll Result:</font> <font color='yellow'>%s</font>" % result)
            return
        elif command == "d12roll":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1,12)
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "<font color='cyan'>D12 Roll Result:</font> <font color='yellow'>%s</font>" % result)
            return
        elif command == "d20roll":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1,20)
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "<font color='cyan'>D20 Roll Result:</font> <font color='yellow'>%s</font>" % result)
            return
        elif command == "customroll":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                all_messages = message[1:].split()
                number_of_dice = int(all_messages[1])
                number_of_faces = int(all_messages[2])
                if(number_of_dice > 20):
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                    "Too many dice! Dice Limit: 20")
                    return 
                ret_text = "<br><font color='red'>Custom Dice Roll:</font>"
                for i in range(number_of_dice):
                    random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
                    result = random.randint(1,number_of_faces)
                    ret_text += "<br><font color='cyan'>[Dice %s]-</font> <font color='yellow'>Rolled %s</font>" % (i, result)
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                    "%s" % ret_text) 
                return
            except (Exception):
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "Incorrect paramaters! Format: !customroll 'number_of_dice' 'dice_faces'")
                return

    @staticmethod
    def plugin_test():
        debug_print("Randomizer Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Randomizer Plugin")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
