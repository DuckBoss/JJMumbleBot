import unittest
from helpers.global_access import GlobalMods as GM
import utils


class Tests(unittest.TestCase):
	def test_version(self):
		# Initialize configs.
        GM.cfg.read(utils.get_tests_dir())
        self.assertEqual(GM.cfg['Bot_Information']['BotVersion'], "v1.8.2")
