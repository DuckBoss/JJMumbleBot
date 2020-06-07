from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.helpers.bot_service_helper import log
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.core.auto_updater.utility import auto_updater_helper as update_utils


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        import os
        import json
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
        self.plugin_cmds = json.loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def get_metadata(self):
        return self.metadata

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "update":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            res = update_utils.update_available(message_parse[1])
            if res is True:
                updated_version = update_utils.check_and_update(message_parse[1])
                if updated_version:
                    GS.gui_service.quick_gui(f"Dependency: [{message_parse[1]} has been updated to v{updated_version}",
                                             text_type='header', box_align='left', ignore_whisper=True)
                    GS.log_service.info(f"Dependency: [{message_parse[1]} has been updated to v{updated_version}")
                    return
                GS.gui_service.quick_gui(f"Dependency: [{message_parse[1]} could not be updated.",
                                         text_type='header', box_align='left', ignore_whisper=True)
                GS.log_service.info(f"Dependency: [{message_parse[1]} could not be updated.")
            elif res is None:
                GS.gui_service.quick_gui(f"The package: [{message_parse[1]}] is not a dependency of this software.",
                                         text_type='header', box_align='left', ignore_whisper=True)
                return
            else:
                GS.gui_service.quick_gui(f"There is no update available for: [{message_parse[1]}].",
                                         text_type='header', box_align='left', ignore_whisper=True)

        elif command == "checkforupdates":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            res = update_utils.update_available(message_parse[1])
            if res is True:
                GS.gui_service.quick_gui(f"There is a newer version of: [{message_parse[1]}] available.",
                                         text_type='header', box_align='left', ignore_whisper=True)
            elif res is None:
                GS.gui_service.quick_gui(f"The package: [{message_parse[1]}] is not a dependency of this software.",
                                         text_type='header', box_align='left', ignore_whisper=True)
            else:
                GS.gui_service.quick_gui(f"There is no update available for: [{message_parse[1]}].",
                                         text_type='header', box_align='left', ignore_whisper=True)
