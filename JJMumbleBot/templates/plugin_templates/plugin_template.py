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
