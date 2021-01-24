import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_extension_plugin_dir
from JJMumbleBot.lib.resources.strings import C_PLUGIN_INFO, P_PLUGIN_VERS, P_PLUGIN_CMDS, C_PLUGIN_SET
from JJMumbleBot.plugins.extensions.text_to_speech.resources.strings import P_TTS_ALL_VOICE, P_TTS_DEF_VOICE, \
    P_TTS_MSG_CHR_LIM
from JJMumbleBot.plugins.extensions.text_to_speech.text_to_speech import Plugin


class TestTextToSpeech:
    def setup_method(self):
        # Initialize configs.
        self.cfg = configparser.ConfigParser()
        self.cfg.read(f"{get_extension_plugin_dir()}/text_to_speech/metadata.ini")

    def test_plugin_version(self):
        assert self.cfg[C_PLUGIN_INFO][P_PLUGIN_VERS] == "4.4.0"

    def test_commands_list_size(self):
        commands_list = list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS]))
        assert len(commands_list) == 7

    def test_match_commands_to_methods(self):
        method_list = [item for item in dir(Plugin) if callable(getattr(Plugin, item)) and item.startswith("cmd_")]
        assert len(method_list) == len(list(loads(self.cfg[C_PLUGIN_INFO][P_PLUGIN_CMDS])))

    def test_text_char_limit(self):
        assert int(self.cfg[C_PLUGIN_SET][P_TTS_MSG_CHR_LIM]) == 256

    def test_default_voice(self):
        assert self.cfg[C_PLUGIN_SET][P_TTS_DEF_VOICE] == "Brian"

    def test_allowed_voice_list(self):
        assert len(list(loads(self.cfg[C_PLUGIN_SET][P_TTS_ALL_VOICE]))) == 57
