import unittest
import sys
sys.path.append(".")
import utils
sys.path.append(".")
from helpers.global_access import GlobalMods as GM


class Tests(unittest.TestCase):
    def setUp(self):
        # Initialize configs.
        GM.cfg.read(f"{utils.get_main_dir()}{utils.get_templates_dir()}/sample_config.ini")
        print(f"{utils.get_main_dir()}{utils.get_templates_dir()}/sample_config.ini")
    def test_version(self):
        GM.cfg.read(f"{utils.get_main_dir()}{utils.get_templates_dir()}/sample_config.ini")
        bot_version = GM.cfg['Bot_Information']['BotVersion']
        self.assertEqual(bot_version, "v1.8.2")


if __name__ == '__main__':
	unittest.main()