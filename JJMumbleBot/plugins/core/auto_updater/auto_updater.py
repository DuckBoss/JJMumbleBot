from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.core.auto_updater.resources.strings import *
from JJMumbleBot.plugins.core.auto_updater.utility import auto_updater_helper as update_utils


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
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

    def cmd_updatedependency(self, data):
        all_data = data.message.strip().split()
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_UPDATE,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR,
                gui_service=gs.gui_service, print_mode=PrintMode.VERBOSE_PRINT.value)
            return
        res = update_utils.update_available(all_data[1])
        if res is True:
            updated_version = update_utils.check_and_update(all_data[1],
                                                            pip_cmd=self.metadata[C_PLUGIN_SET][P_PIP_CMD])
            if updated_version:
                log(
                    INFO,
                    f"Dependency: [{all_data[1]}] has been updated to v{updated_version}",
                    origin=L_DEPENDENCIES,
                    gui_service=gs.gui_service,
                    print_mode=PrintMode.VERBOSE_PRINT.value
                )
                return
            log(
                WARNING,
                f"Dependency: [{all_data[1]}] could not be updated.",
                origin=L_DEPENDENCIES,
                gui_service=gs.gui_service,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
        elif res is None:
            log(
                WARNING,
                f"The package: [{all_data[1]}] is not a dependency of this software.",
                origin=L_DEPENDENCIES,
                gui_service=gs.gui_service,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            return
        else:
            log(
                INFO,
                f"There is no update available for: [{all_data[1]}].",
                origin=L_DEPENDENCIES,
                gui_service=gs.gui_service,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )

    def cmd_checkforupdates(self, data):
        all_data = data.message.strip().split()
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_CHECK,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR,
                gui_service=gs.gui_service, print_mode=PrintMode.VERBOSE_PRINT.value)
            return
        res = update_utils.update_available(all_data[1])
        if res is True:
            gs.gui_service.quick_gui(f"There is a newer version of: [{all_data[1]}] available.",
                                     text_type='header', box_align='left', ignore_whisper=True)
        elif res is None:
            log(
                WARNING,
                f"The package: [{all_data[1]}] is not a dependency of this software.",
                origin=L_DEPENDENCIES,
                gui_service=gs.gui_service,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
        else:
            log(
                INFO,
                f"There is no update available for: [{all_data[1]}].",
                origin=L_DEPENDENCIES,
                gui_service=gs.gui_service,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
