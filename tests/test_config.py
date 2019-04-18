import unittest
import sys
sys.path.append(".")
import utils
sys.path.append(".")
from helpers.global_access import GlobalMods as GM


class Tests(unittest.TestCase):
    def setUp(self):
        # Initialize configs.
        GM.cfg.read(f"{utils.get_tests_dir()}/sample_config.ini")
    def test_version(self):
        self.assertEqual(GM.cfg['Bot_Information']['BotVersion'], "v1.8.2")


if __name__ == '__main__':
	unittest.main()