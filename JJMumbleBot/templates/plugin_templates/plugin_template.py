from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import rprint, dprint


class Plugin(PluginBase):
    # Initializes the plugin with the main core information.
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.is_running = True
        # Add any custom initialization code here...
        # ...
        # ...
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    # This is the standard quit method that is called when the bot is shutting down.
    # Don't modify this method unless you need to conduct some clean-up before the plugin exits.
    def quit(self):
        self.is_running = False
        dprint(f"Exiting {self.plugin_name} plugin...")
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

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

    # Each command must be it's own method definition
    # All command methods must be prefixed with 'cmd' and require 'self','data' in the parameters.
    # Example: !my_echo_command -> def cmd_mycommand(self, data)
    # You can use the 'data' parameter to extract information such as the command name/message body.
    # Example: !my_echo_command blah blah blah
    #          data.command -> my_echo_command
    #          data.message -> !my_echo_command blah blah blah
    def cmd_my_echo_command(self, data):
        text_to_echo = data.message.strip().split(' ', 1)[1]
        global_settings.gui_service.quick_gui(text_to_echo, text_type='header', box_align='left', ignore_whisper=True)
        log(INFO, f"Echo:[{text_to_echo}]", origin=L_GENERAL)
