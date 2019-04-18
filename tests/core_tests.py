import unittest
import sys
import utils
sys.path.append("..")
from helpers.global_access import GlobalMods as GM


class Tests(unittest.TestCase):
    def test_version(self):
        # Initialize configs.
        GM.cfg.read(f"{utils.get_tests_dir()}/sample_config.ini")
        self.assertEqual(GM.cfg['Bot_Information']['BotVersion'], "v1.8.2")
