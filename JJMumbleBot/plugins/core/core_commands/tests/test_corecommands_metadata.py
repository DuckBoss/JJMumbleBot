import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_core_plugin_dir
from JJMumbleBot.lib.resources.strings import C_PLUGIN_INFO, P_PLUGIN_VERS, P_PLUGIN_CMDS
from JJMumbleBot.plugins.core.core_commands.core_commands import Plugin


class TestCoreCommands:
    def setup_method(self):
        # Initialize configs.
        self.cfg = configparser.ConfigParser()
        self.cfg.read(f"{get_core_plugin_dir()}/core_commands/metadata.ini")

    def test_plugin_version(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_VERS] == "5.2.0"

    def test_commands_list_size(self):
        commands_list = list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS]))
        assert len(commands_list) == 29

    def test_match_commands_to_methods(self):
        method_list = [item for item in dir(Plugin) if callable(getattr(Plugin, item)) and item.startswith("cmd_")]
        assert len(method_list) == len(list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS])))
