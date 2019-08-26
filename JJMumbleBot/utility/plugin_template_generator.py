import os
import sys
from JJMumbleBot.lib.utils import dir_utils

py_template = """
from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib import privileges


class Plugin(PluginBase):
    def quit(self):
        dprint("Exiting Plugin...")

    def get_metadata(self):
        return self.metadata

    def __init__(self):
        super().__init__()
        import os
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
        
        if command == "example_echo":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = message_parse[1]
            global_settings.gui_service.quick_gui(parameter, text_type='header', box_align='left', ignore_whisper=True)
            global_settings.log_service.info(f"Echo:[{parameter}]")
            return

"""
help_template = """
All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>
<b>!example_echo 'message/images'</b>: Echoes a message/images in the chat.
"""
meta_template = """
[Plugin Information]
PluginVersion = 1.0.0
PluginName = Example
PluginDescription = Default plugin description.
PluginLanguage = EN
PluginCommands: [
                "example_echo"
                ]

[Plugin Type]
AudioPlugin = False
ImagePlugin = False
CorePlugin = False
ExtensionPlugin = True

[Plugin Requirements]
RequiresCore = False
RequiresUserPermissions = true
RequiresHelpData = true
RequiresImageProcessing = false
RequiresAudioProcessing = false
RequiresOtherPlugins = false
RequiresWebInterface = false
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
