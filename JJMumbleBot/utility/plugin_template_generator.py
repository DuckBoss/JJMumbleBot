import os
import sys
from JJMumbleBot.lib.utils import dir_utils


py_template = """
from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib import privileges


class Plugin(PluginBase):
    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...")
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def get_metadata(self):
        return self.metadata

    def __init__(self):
        super().__init__()
        import os
        import json
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = json.loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]
        
        if command == "example_echo":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            parameter = message_parse[1]
            global_settings.gui_service.quick_gui(parameter, text_type='header', box_align='left', ignore_whisper=True)
            log(INFO, f"Echo:[{parameter}]", origin=L_GENERAL)
            return

"""
help_template = """
All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>
<b>!example_echo 'message/images'</b>: Echoes a message/images in the chat.
"""
meta_template = """
[Plugin Information]
PluginVersion = 1.0.0
PluginName = Plugin Name
PluginDescription = Plugin Description
PluginLanguage = EN
PluginCommands: []

[Plugin Settings]
; List commands that need the core thread to wait for completion.
; This may include processes that require multiple commands in succession.
; For example: [Youtube Plugin - !yt -> !p] process requires 2 commands in that order.
ThreadWaitForCommands: []
; Finishes the task before continuing the bot service process.
UseSingleThread = False

[Plugin Type]
AudioPlugin = False
ImagePlugin = False
CorePlugin = False
ExtensionPlugin = True
"""
priv_template = """
command,level
example_echo,1
"""


def create_new_template(plugin_name: str):
    formatted_name = plugin_name.strip().replace(" ", "_")
    dir_utils.make_directory(f'{dir_utils.get_main_dir()}/user_generated/plugins/{formatted_name}')
    dir_utils.clear_directory(f'{dir_utils.get_main_dir()}/user_generated/plugins/{formatted_name}')
    with open(
            f'{dir_utils.get_main_dir()}/user_generated/plugins/{formatted_name}/{formatted_name.lower()}.py',
            'w+') as f:
        f.write(py_template)
    with open(
            f'{dir_utils.get_main_dir()}/user_generated/plugins/{formatted_name}/help.html',
            'w+') as f:
        f.write(help_template)
    with open(
            f'{dir_utils.get_main_dir()}/user_generated/plugins/{formatted_name}/metadata.ini',
            'w+') as f:
        f.write(meta_template)
    with open(
            f'{dir_utils.get_main_dir()}/user_generated/plugins/{formatted_name}/privileges.csv',
            'w+') as f:
        f.write(priv_template)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        create_new_template(sys.argv[1])
    else:
        print('Incorrect Format: python3 plugin_template_generator my_plugin_name')
