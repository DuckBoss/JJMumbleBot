import sys
from JJMumbleBot.lib.utils import dir_utils

py_template = """
from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *


class Plugin(PluginBase):
    # Initializes the plugin with the main core information.
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        # Add any custom initialization code here...
        # ...
        # ...
        self.register_callbacks()
        self.is_running = True
        log(INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value)

    # This is the standard quit method that is called when the bot is shutting down.
    # Don't modify this method unless you need to conduct some clean-up before the plugin exits.
    def quit(self):
        self.is_running = False
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN, print_mode=PrintMode.REG_PRINT.value)

    # This method is called when a controllable plugin is requested to stop from a command.
    # Do not modify this command unless you need to conduct some clean-up before the plugin exits.
    def stop(self):
        if self.is_running:
            self.quit()

    # This method is called when a controllable plugin is requested to start from a command.
    # Do not modify this command unless you need to initialize data before starting the plugin.
    def start(self):
        if not self.is_running:
            self.__init__()
            
    # This method is used to register plugin-specific callbacks for event-driven actions.
    # For example, in the media plugin, there are multiple callbacks registered to handle
    # the automatic downloading of thumbnail images and sequencing of tracks.
    # Since the implementation of a plugin's callbacks are unique to the plugin, this template leaves this blank.
    # In addition, not all plugins require callbacks to be registered and is dependent on the use-case.
    def register_callbacks(self):
        pass

    # Each command must be its own method definition
    # All command methods must be prefixed with 'cmd_' and require 'self','data' in the parameters.
    # Example: !example_echo -> def cmd_example_echo(self, data)
    # You can use the 'data' parameter to extract information such as the command name/message body.
    # Example: !example_echo blah blah blah
    #          data.command -> example_echo
    #          data.message -> !example_echo blah blah blah
    def cmd_example_echo(self, data):
        text_to_echo = data.message.strip().split(' ', 1)[1]
        gs.gui_service.quick_gui(text_to_echo, text_type='header', box_align='left', ignore_whisper=True)
        log(INFO, f"Echo:[{text_to_echo}]", origin=L_GENERAL)
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
PluginCommands: ["example_echo"]

[Plugin Settings]
; List commands that need the core thread to wait for completion.
; This may include processes that require multiple commands in succession.
; For example: [Youtube Plugin - !yt -> !p] process requires 2 commands in that order.
ThreadWaitForCommands: []
; Finishes the task before continuing the bot service process.
UseSingleThread = False

[Plugin Type]
ControllablePlugin = False
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
