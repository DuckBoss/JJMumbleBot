import unittest
import sys
import os
sys.path.append(".")
import utils
sys.path.append(".")
from helpers.global_access import GlobalMods as GM


class Tests(unittest.TestCase):
    def setUp(self):
        # Initialize configs.
        GM.cfg.read(f"{utils.get_main_dir()}{utils.get_templates_dir()}/sample_config.ini")
        # Initialize plugins.
        self.bot_plugins = {}
        sys.path.insert(0, f"{utils.get_main_dir()}/plugins/")
        all_imports = [name for name in os.listdir(f"{utils.get_main_dir()}/plugins/") if os.path.isdir(os.path.join(f"{utils.get_main_dir()}/plugins/", name)) and name != "__pycache__"]
        for p_file in all_imports:
            if p_file == "help":
                self.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin("")
                continue
            self.bot_plugins[p_file] = __import__(f'{p_file}.{p_file}', fromlist=['*']).Plugin()
        sys.path.pop(0)

    def test_version_help(self):
        cur_plugin = self.bot_plugins.get('help')
        self.assertEqual(cur_plugin.get_plugin_version(), "2.0.0")

    def test_version_randomizer(self):
        cur_plugin = self.bot_plugins.get('randomizer')
        self.assertEqual(cur_plugin.get_plugin_version(), "2.0.0")

    def test_version_bot_commands(self):
        cur_plugin = self.bot_plugins.get('bot_commands')
        self.assertEqual(cur_plugin.get_plugin_version(), "2.0.0")

    def test_version_youtube(self):
        cur_plugin = self.bot_plugins.get('youtube')
        self.assertEqual(cur_plugin.get_plugin_version(), "2.0.0")

    def test_version_sound_board(self):
        cur_plugin = self.bot_plugins.get('sound_board')
        self.assertEqual(cur_plugin.get_plugin_version(), "2.0.1")

    def test_version_images(self):
        cur_plugin = self.bot_plugins.get('images')
        self.assertEqual(cur_plugin.get_plugin_version(), "2.0.0")


if __name__ == '__main__':
    unittest.main()
