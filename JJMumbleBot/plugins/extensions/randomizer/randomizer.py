from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.plugins.extensions.randomizer.resources.strings import CMD_INVALID_CUSTOM_ROLL
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *
import os
import random


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        log(
            INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value
        )

    def quit(self):
        log(
            INFO,
            f"Exiting {self.plugin_name} plugin...",
            origin=L_SHUTDOWN,
            print_mode=PrintMode.REG_PRINT.value
        )

    def cmd_coinflip(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = "Heads" if random.randint(1, 2) == 1 else "Tails"
        log(INFO, "Simulated a random coin flip and displayed the results.",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui(
            f"<font color='cyan'>Coin Flip Result:</font> <font color='yellow'>{result}</font>",
            text_type='header', box_align='left')

    def cmd_d4roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 4)
        log(INFO, "Simulated a random d4 dice roll and displayed the results.",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui(f"<font color='cyan'>D4 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d6roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 6)
        log(INFO, "Simulated a random d6 dice roll and displayed the results.",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui(f"<font color='cyan'>D6 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d8roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 8)
        log(INFO, "Simulated a random d8 dice roll and displayed the results.",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui(f"<font color='cyan'>D8 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d10roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 10)
        gs.gui_service.quick_gui(f"<font color='cyan'>D10 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d12roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 12)
        log(INFO, "Simulated a random d12 dice roll and displayed the results.",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui(f"<font color='cyan'>D12 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d16roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 16)
        gs.gui_service.quick_gui(f"<font color='cyan'>D16 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d20roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 20)
        log(INFO, "Simulated a random d20 dice roll and displayed the results.",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui(f"<font color='cyan'>D20 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_d100roll(self, data):
        random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
        result = random.randint(1, 100)
        log(INFO, "Simulated a random d100 dice roll and displayed the results.",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui(f"<font color='cyan'>D100 Roll Result:</font> <font color='yellow'>{result}</font>",
                                 text_type='header', box_align='left')

    def cmd_customroll(self, data):
        all_data = data.message.strip().split()
        try:
            number_of_dice = int(all_data[1])
            number_of_faces = int(all_data[2])
            if number_of_dice > 20:
                gs.gui_service.quick_gui("Too many dice! Dice Limit: 20",
                                         text_type='header', box_align='left')
                return
            ret_text = "<br><font color='red'>Custom Dice Roll:</font>"
            for i in range(number_of_dice):
                random.seed(int.from_bytes(os.urandom(8), byteorder="big"))
                result = random.randint(1, number_of_faces)
                ret_text += f"<br><font color='cyan'>[Dice {i}]-</font> <font color='yellow'>Rolled {result}</font>"
            gs.gui_service.quick_gui(ret_text, text_type='header', box_align='left')
            return
        except IndexError:
            log(ERROR, CMD_INVALID_CUSTOM_ROLL,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(CMD_INVALID_CUSTOM_ROLL,
                                     text_type='header', box_align='left')
            return
