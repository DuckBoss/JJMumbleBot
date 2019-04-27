from templates.plugin_template import PluginBase
from helpers.global_access import debug_print
from helpers.global_access import GlobalMods as GM
import privileges as pv
import os
import random


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the chat or privately messaging JJMumbleBot.<br>\
                <b>!customroll 'number_of_dice' 'dice_faces'</b>: A custom dice roll with multiple dice and custom face counts.<br>\
                <b>!coinflip</b>: A coin flip 2-sided roll.<br>\
                <b>!d4roll</b>: A standard 4-sided dice roll.<br>\
                <b>!d6roll</b>: A standard 6-sided dice roll.<br>\
                <b>!d8roll</b>: A standard 8-sided dice roll.<br>\
                <b>!d10roll</b>: A standard 10-sided dice roll.<br>\
                <b>!d12roll</b> A standard 12-sided dice roll.<br>\
                <b>!d20roll</b> A standard 20-sided dice roll."
    plugin_version = "2.0.0"
    priv_path = "randomizer/randomizer_privileges.csv"

    def __init__(self):
        debug_print("Randomizer Plugin Initialized.")
        super().__init__()

    def process_command(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "coinflip":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 2)
            if result == 1:
                result = "Heads"
            else:
                result = "Tails"
            GM.gui.quick_gui(f"<font color='cyan'>Coin Flip Result:</font> <font color='yellow'>{result}</font>",
                             text_type='header', box_align='left')
            return
        elif command == "d4roll":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 4)
            GM.gui.quick_gui(f"<font color='cyan'>D4 Roll Result:</font> <font color='yellow'>{result}</font>",
                             text_type='header', box_align='left')
            return
        elif command == "d6roll":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 6)
            GM.gui.quick_gui(f"<font color='cyan'>D6 Roll Result:</font> <font color='yellow'>{result}</font>",
                             text_type='header', box_align='left')
            return
        elif command == "d8roll":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 8)
            GM.gui.quick_gui(f"<font color='cyan'>D8 Roll Result:</font> <font color='yellow'>{result}</font>",
                             text_type='header', box_align='left')
            return
        elif command == "d10roll":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 10)
            GM.gui.quick_gui(f"<font color='cyan'>D10 Roll Result:</font> <font color='yellow'>{result}</font>",
                             text_type='header', box_align='left')
            return
        elif command == "d12roll":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 12)
            GM.gui.quick_gui(f"<font color='cyan'>D12 Roll Result:</font> <font color='yellow'>{result}</font>",
                             text_type='header', box_align='left')
            return
        elif command == "d20roll":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 20)
            GM.gui.quick_gui(f"<font color='cyan'>D20 Roll Result:</font> <font color='yellow'>{result}</font>",
                             text_type='header', box_align='left')
            return
        elif command == "customroll":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                all_messages = message[1:].split()
                number_of_dice = int(all_messages[1])
                number_of_faces = int(all_messages[2])
                if number_of_dice > 20:
                    GM.gui.quick_gui("Too many dice! Dice Limit: 20",
                                     text_type='header', box_align='left')
                    return 
                ret_text = "<br><font color='red'>Custom Dice Roll:</font>"
                for i in range(number_of_dice):
                    random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
                    result = random.randint(1, number_of_faces)
                    ret_text += f"<br><font color='cyan'>[Dice {i}]-</font> <font color='yellow'>Rolled {result}</font>"
                GM.gui.quick_gui(ret_text, text_type='header', box_align='left')
                return
            except Exception:
                GM.gui.quick_gui("Incorrect paramaters! Format: !customroll 'number_of_dice' 'dice_faces'",
                                 text_type='header', box_align='left')
                return

    def plugin_test(self):
        debug_print("Randomizer Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Randomizer Plugin")

    def help(self):
        return self.help_data

    def is_audio_plugin(self):
        return False

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
