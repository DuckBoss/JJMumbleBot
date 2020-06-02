from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *
import os
import random


class Plugin(PluginBase):
    def get_metadata(self):
        pass

    def __init__(self):
        super().__init__()
        import json
        raw_file = os.path.basename(__file__)
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{raw_file}')
        self.plugin_cmds = json.loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.priv_path = f'plugins/extensions/{raw_file.split(".")[0]}/privileges.csv'
        self.help_path = f'plugins/extensions/{raw_file.split(".")[0]}/help.html'
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "coinflip":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 2)
            if result == 1:
                result = "Heads"
            else:
                result = "Tails"
            GS.gui_service.quick_gui(
                f"<font color='cyan'>Coin Flip Result:</font> <font color='yellow'>{result}</font>",
                text_type='header', box_align='left')
            return
        elif command == "d4roll":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 4)
            GS.gui_service.quick_gui(f"<font color='cyan'>D4 Roll Result:</font> <font color='yellow'>{result}</font>",
                                     text_type='header', box_align='left')
            return
        elif command == "d6roll":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 6)
            GS.gui_service.quick_gui(f"<font color='cyan'>D6 Roll Result:</font> <font color='yellow'>{result}</font>",
                                     text_type='header', box_align='left')
            return
        elif command == "d8roll":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 8)
            GS.gui_service.quick_gui(f"<font color='cyan'>D8 Roll Result:</font> <font color='yellow'>{result}</font>",
                                     text_type='header', box_align='left')
            return
        elif command == "d10roll":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 10)
            GS.gui_service.quick_gui(f"<font color='cyan'>D10 Roll Result:</font> <font color='yellow'>{result}</font>",
                                     text_type='header', box_align='left')
            return
        elif command == "d12roll":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 12)
            GS.gui_service.quick_gui(f"<font color='cyan'>D12 Roll Result:</font> <font color='yellow'>{result}</font>",
                                     text_type='header', box_align='left')
            return
        elif command == "d20roll":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
            result = random.randint(1, 20)
            GS.gui_service.quick_gui(f"<font color='cyan'>D20 Roll Result:</font> <font color='yellow'>{result}</font>",
                                     text_type='header', box_align='left')
            return
        elif command == "customroll":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                all_messages = message[1:].split()
                number_of_dice = int(all_messages[1])
                number_of_faces = int(all_messages[2])
                if number_of_dice > 20:
                    GS.gui_service.quick_gui("Too many dice! Dice Limit: 20",
                                             text_type='header', box_align='left')
                    return
                ret_text = "<br><font color='red'>Custom Dice Roll:</font>"
                for i in range(number_of_dice):
                    random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
                    result = random.randint(1, number_of_faces)
                    ret_text += f"<br><font color='cyan'>[Dice {i}]-</font> <font color='yellow'>Rolled {result}</font>"
                GS.gui_service.quick_gui(ret_text, text_type='header', box_align='left')
                return
            except Exception:
                GS.gui_service.quick_gui("Incorrect parameters! Format: !customroll 'number_of_dice' 'dice_faces'",
                                         text_type='header', box_align='left')
                return

    def quit(self):
        dprint("Exiting Randomizer Plugin")