from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib import privileges


class Plugin(PluginBase):
    # Don't modify this method unless you need to conduct some clean-up before the plugin exits.
    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...")
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    # Don't modify this method.
    def get_metadata(self):
        return self.metadata

    # Initializes the plugin with the main core information.
    def __init__(self):
        super().__init__()
        import os
        import json
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = json.loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        # Add any custom initialization code here...
        # ...
        # ...
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    # The main method to process incoming commands to the plugin.
    def process(self, text):
        # By default, the method creates some variables that separate the command from the rest of the parameters.
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        # A basic example command, using the if-else structure.
        if command == "example_echo":
            # Always check the user privileges at the start of your command processing.
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return

            parameter = message_parse[1]
            global_settings.gui_service.quick_gui(parameter, text_type='header', box_align='left', ignore_whisper=True)
            log(INFO, f"Echo:[{parameter}]", origin=L_GENERAL)
            return
