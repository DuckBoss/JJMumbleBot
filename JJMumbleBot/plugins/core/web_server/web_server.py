from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.core.web_server.web_helper import initialize_web
from JJMumbleBot.plugins.core.web_server.monitor_service import get_server_hierarchy


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.is_running = True
        initialize_web()
        log(
            INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value
        )

    def stop_server(self):
        if gs.data_server:
            gs.data_server.stop()
            log(INFO, f"Terminating web server instance", origin=L_SHUTDOWN, print_mode=PrintMode.REG_PRINT.value)
            gs.data_server = None

    def start_server(self):
        if not gs.data_server:
            initialize_web()
            log(INFO, f"Initializing new web server instance", origin=L_SHUTDOWN, print_mode=PrintMode.REG_PRINT.value)
        log(INFO, f"Web Server instance already exists!", origin=L_SHUTDOWN,
            print_mode=PrintMode.REG_PRINT.value)

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

    def cmd_testserver(self, data):
        get_server_hierarchy()
