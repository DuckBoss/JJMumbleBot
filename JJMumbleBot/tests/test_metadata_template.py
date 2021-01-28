import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_main_dir
from JJMumbleBot.lib.resources.strings import *


class TestMetadataTemplate:
    def setup_method(self):
        # Initialize metadata.
        self.cfg = configparser.ConfigParser()
        self.cfg.read(f"{get_main_dir()}/templates/plugin_templates/metadata_template.ini")

    # Plugin Information Tests
    def test_plugin_version(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_VERS] == "1.0.0"

    def test_plugin_name(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_NAME] == "Plugin Name"

    def test_plugin_description(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_DESC] == "Plugin Description"

    def test_plugin_language(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_LANG] == "EN"

    def test_plugin_commands(self):
        assert len(list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS]))) == 0

    # Plugin Settings Tests
    def test_thread_wait_for_commands(self):
        assert len(list(loads(self.cfg[C_PLUGIN_SET][P_THREAD_WAIT]))) == 0

    def test_use_single_thread(self):
        assert self.cfg.getboolean(C_PLUGIN_SET, P_THREAD_SINGLE) is False

    # Plugin Type Tests
    def test_is_controllable(self):
        assert self.cfg.getboolean(C_PLUGIN_TYPE, P_CTR_PLUGIN) is False

    def test_is_audio(self):
        assert self.cfg.getboolean(C_PLUGIN_TYPE, P_AUD_PLUGIN) is False

    def test_is_image(self):
        assert self.cfg.getboolean(C_PLUGIN_TYPE, P_IMG_PLUGIN) is False

    def test_is_core(self):
        assert self.cfg.getboolean(C_PLUGIN_TYPE, P_CORE_PLUGIN) is False

    def test_is_extension(self):
        assert self.cfg.getboolean(C_PLUGIN_TYPE, P_EXT_PLUGIN) is True
