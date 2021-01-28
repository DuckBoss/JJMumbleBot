import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_core_plugin_dir
from JJMumbleBot.lib.resources.strings import C_PLUGIN_INFO, P_PLUGIN_VERS, P_PLUGIN_CMDS, C_PLUGIN_SET
from JJMumbleBot.plugins.core.web_server.resources.strings import P_WEB_PORT, P_WEB_ENABLE, P_WEB_IP, P_WEB_TICK_RATE
from JJMumbleBot.plugins.core.web_server.web_server import Plugin


class TestWebServer:
    def setup_method(self):
        # Initialize configs.
        self.cfg = configparser.ConfigParser()
        self.cfg.read(f"{get_core_plugin_dir()}/web_server/metadata.ini")

    def test_plugin_version(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_VERS] == "5.0.0"

    def test_commands_list_size(self):
        commands_list = list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS]))
        assert len(commands_list) == 2

    def test_match_commands_to_methods(self):
        method_list = [item for item in dir(Plugin) if callable(getattr(Plugin, item)) and item.startswith("cmd_")]
        assert len(method_list) == len(list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS])))

    def test_web_interface(self):
        enable_web_interface = self.cfg.getboolean(C_PLUGIN_SET, P_WEB_ENABLE)
        assert enable_web_interface is True

    def test_web_ip(self):
        web_server_ip = self.cfg[C_PLUGIN_SET][P_WEB_IP]
        assert web_server_ip == "0.0.0.0"

    def test_web_port(self):
        web_server_port = int(self.cfg[C_PLUGIN_SET][P_WEB_PORT])
        assert web_server_port == 7000

    def test_web_tick_rate(self):
        web_tick_rate = int(self.cfg[C_PLUGIN_SET][P_WEB_TICK_RATE])
        assert web_tick_rate == 1
