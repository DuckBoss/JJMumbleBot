from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.core.web_server.web_helper import initialize_web
from JJMumbleBot.plugins.core.web_server.utility import settings as ws_settings
from JJMumbleBot.plugins.core.web_server.resources.strings import *


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        if gs.safe_mode is True:
            log(INFO, "The web_server plugin cannot be started in safe mode. Skipping initialization...",
                origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)
            return

        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        ws_settings.web_server_metadata = self.metadata
        ws_settings.plugin_name = self.plugin_name
        self.is_running = True
        log(INFO, "######### Configuring Web Interface #########",
            origin=L_WEB_INTERFACE, print_mode=PrintMode.VERBOSE_PRINT.value)
        from JJMumbleBot.lib.database import InsertDB
        from JJMumbleBot.lib.utils.database_management_utils import get_memory_db
        from JJMumbleBot.lib.privileges import Privileges
        if InsertDB.insert_new_user(db_conn=get_memory_db(),
                                    username=gs.cfg[C_CONNECTION_SETTINGS][P_USER_ID]):
            InsertDB.insert_new_permission(db_conn=get_memory_db(),
                                           username=gs.cfg[C_CONNECTION_SETTINGS][P_USER_ID],
                                           permission_level=int(Privileges.SUPERUSER.value))
        log(INFO, "######### Configured Web Interface #########",
            origin=L_WEB_INTERFACE, print_mode=PrintMode.VERBOSE_PRINT.value)
        if self.metadata.getboolean(C_PLUGIN_SET, P_WEB_ENABLE, fallback=False):
            initialize_web(self.metadata[C_PLUGIN_SET][P_WEB_IP], self.metadata[C_PLUGIN_SET][P_WEB_PORT])
        log(
            INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value
        )

    def stop_server(self):
        if gs.data_server:
            gs.data_server.stop()
            log(INFO, f"Terminating web server instance", origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)
            gs.data_server = None

    def start_server(self):
        if not gs.data_server:
            initialize_web(self.metadata[C_PLUGIN_SET][P_WEB_IP], self.metadata[C_PLUGIN_SET][P_WEB_PORT])
            log(INFO, f"Initializing new web server instance", origin=L_WEB_INTERFACE, print_mode=PrintMode.REG_PRINT.value)
            gs.gui_service.quick_gui(
                f"Initializing new web server instance",
                text_type='header',
                box_align='left')
        else:
            log(INFO, f"Web Server instance already exists!", origin=L_WEB_INTERFACE,
                print_mode=PrintMode.REG_PRINT.value)
            gs.gui_service.quick_gui(
                f"Web Server instance already exists!",
                text_type='header',
                box_align='left')

    def quit(self):
        self.stop_server()
        self.is_running = False
        log(
            INFO,
            f"Exiting {self.plugin_name} plugin...",
            origin=L_SHUTDOWN,
            print_mode=PrintMode.REG_PRINT.value
        )

    def stop(self):
        if self.is_running:
            self.quit()

    def start(self):
        if not self.is_running:
            self.__init__()

    def cmd_stopwebserver(self, data):
        self.stop_server()

    def cmd_startwebserver(self, data):
        self.start_server()
