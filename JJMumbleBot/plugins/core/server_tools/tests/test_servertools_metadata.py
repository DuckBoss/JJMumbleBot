import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_core_plugin_dir
from JJMumbleBot.lib.resources.strings import C_PLUGIN_INFO, P_PLUGIN_VERS, P_PLUGIN_CMDS, C_PLUGIN_SET
from JJMumbleBot.plugins.core.server_tools.resources.strings import P_USE_WELCOME_MSG, P_WELCOME_MSG, \
    P_PLAY_SAME_CLIP_ON_USER_JOIN, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, \
    P_PLAY_CLIP_ONLY_IF_USERS_IN_CHANNEL, P_GENERIC_CLIP_TO_PLAY_ON_USER_JOIN,\
    P_USE_SOUNDBOARD_CLIPS, P_USE_BUILT_IN_CLIP
from JJMumbleBot.plugins.core.server_tools.server_tools import Plugin


class TestServerTools:
    def setup_method(self):
        # Initialize configs.
        self.cfg = configparser.ConfigParser()
        self.cfg.read(f"{get_core_plugin_dir()}/server_tools/metadata.ini")

    def test_plugin_version(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_VERS] == "4.4.0"

    def test_commands_list_size(self):
        commands_list = list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS]))
        assert len(commands_list) == 5

    def test_match_commands_to_methods(self):
        method_list = [item for item in dir(Plugin) if callable(getattr(Plugin, item)) and item.startswith("cmd_")]
        assert len(method_list) == len(list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS])))

    def test_welcome_message_enabled(self):
        assert self.cfg.getboolean(C_PLUGIN_SET, P_USE_WELCOME_MSG, fallback=False) is True

    def test_welcome_message(self):
        assert self.cfg[C_PLUGIN_SET][P_WELCOME_MSG] == "Hello! Welcome to the server."

    def test_audio_clip_on_user_join(self):
        assert self.cfg.getboolean(C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False) is True

    def test_audio_clip_if_users_in_channel(self):
        assert self.cfg.getboolean(C_PLUGIN_SET, P_PLAY_CLIP_ONLY_IF_USERS_IN_CHANNEL, fallback=False) is True

    def test_same_audio_clip_on_join(self):
        assert self.cfg.getboolean(C_PLUGIN_SET, P_PLAY_SAME_CLIP_ON_USER_JOIN, fallback=False) is False

    def test_generic_audio_clip(self):
        assert len(self.cfg[C_PLUGIN_SET][P_GENERIC_CLIP_TO_PLAY_ON_USER_JOIN]) == 0

    def test_use_built_in_clip(self):
        assert self.cfg.getboolean(C_PLUGIN_SET, P_USE_BUILT_IN_CLIP, fallback=False) is True

    def test_use_sound_board_clips(self):
        assert self.cfg.getboolean(C_PLUGIN_SET, P_USE_SOUNDBOARD_CLIPS, fallback=False) is True
