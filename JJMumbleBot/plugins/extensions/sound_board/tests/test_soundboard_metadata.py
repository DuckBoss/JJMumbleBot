import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_extension_plugin_dir
from JJMumbleBot.lib.resources.strings import C_PLUGIN_INFO, P_PLUGIN_VERS, P_PLUGIN_CMDS, C_PLUGIN_SET
from JJMumbleBot.plugins.extensions.sound_board.resources.strings import P_FUZZY_SEARCH_THRESHOLD, \
    P_MAX_SEARCH_RESULTS, P_ENABLE_QUEUE
from JJMumbleBot.plugins.extensions.sound_board.sound_board import Plugin


class TestSoundBoard:
    def setup_method(self):
        # Initialize configs.
        self.cfg = configparser.ConfigParser()
        self.cfg.read(f"{get_extension_plugin_dir()}/sound_board/metadata.ini")

    def test_plugin_version(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_VERS] == "5.0.0"

    def test_commands_list_size(self):
        commands_list = list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS]))
        assert len(commands_list) == 12

    def test_match_commands_to_methods(self):
        method_list = [item for item in dir(Plugin) if callable(getattr(Plugin, item)) and item.startswith("cmd_")]
        assert len(method_list) == len(list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS])))

    def test_queue_enabled(self):
        assert self.cfg.getboolean(C_PLUGIN_SET, P_ENABLE_QUEUE, fallback=False) is True

    def test_max_search_results(self):
        assert int(self.cfg[C_PLUGIN_SET][P_MAX_SEARCH_RESULTS]) == 5

    def test_fuzzy_Search_threshold(self):
        assert int(self.cfg[C_PLUGIN_SET][P_FUZZY_SEARCH_THRESHOLD]) == 80
