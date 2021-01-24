import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_extension_plugin_dir
from JJMumbleBot.lib.resources.strings import C_PLUGIN_INFO, P_PLUGIN_VERS, P_PLUGIN_CMDS, C_PLUGIN_SET
from JJMumbleBot.plugins.extensions.media.resources.strings import P_YT_MAX_PLAY_LEN, P_YT_ALL_PLAY_MAX, \
    P_YT_MAX_VID_LEN, P_YT_MAX_SEARCH_LEN
from JJMumbleBot.plugins.extensions.media.media import Plugin


class TestMedia:
    def setup_method(self):
        # Initialize configs.
        self.cfg = configparser.ConfigParser()
        self.cfg.read(f"{get_extension_plugin_dir()}/media/metadata.ini")

    def test_plugin_version(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_VERS] == "4.4.0"

    def test_commands_list_size(self):
        commands_list = list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS]))
        assert len(commands_list) == 5

    def test_match_commands_to_methods(self):
        method_list = [item for item in dir(Plugin) if callable(getattr(Plugin, item)) and item.startswith("cmd_")]
        assert len(method_list) == len(list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS])))

    def test_max_search_length(self):
        assert int(self.cfg[C_PLUGIN_SET][P_YT_MAX_SEARCH_LEN]) == 10

    def test_max_vid_length(self):
        assert int(self.cfg[C_PLUGIN_SET][P_YT_MAX_VID_LEN]) == 7000

    def test_max_playlist_length(self):
        assert int(self.cfg[C_PLUGIN_SET][P_YT_MAX_PLAY_LEN]) == 50

    def test_allow_playlist_max(self):
        assert self.cfg.getboolean(C_PLUGIN_SET, P_YT_ALL_PLAY_MAX, fallback=False) is True
