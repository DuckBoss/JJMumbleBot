import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_extension_plugin_dir
from JJMumbleBot.lib.resources.strings import C_PLUGIN_INFO, P_PLUGIN_VERS, P_PLUGIN_CMDS, C_PLUGIN_SET
from JJMumbleBot.plugins.extensions.images.images import Plugin
from JJMumbleBot.plugins.extensions.images.resources.strings import P_FRAME_COL, P_FRAME_SIZE


class TestImages:
    def setup_method(self):
        # Initialize configs.
        self.cfg = configparser.ConfigParser()
        self.cfg.read(f"{get_extension_plugin_dir()}/images/metadata.ini")

    def test_plugin_version(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_VERS] == "5.0.0"

    def test_commands_list_size(self):
        commands_list = list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS]))
        assert len(commands_list) == 4

    def test_match_commands_to_methods(self):
        method_list = [item for item in dir(Plugin) if callable(getattr(Plugin, item)) and item.startswith("cmd_")]
        assert len(method_list) == len(list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS])))

    def test_image_frame_size(self):
        assert int(self.cfg[C_PLUGIN_SET][P_FRAME_SIZE]) == 5

    def test_image_frame_color(self):
        assert self.cfg[C_PLUGIN_SET][P_FRAME_COL] == "black"
