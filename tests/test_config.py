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
    def test_version(self):
        bot_version = GM.cfg['Bot_Information']['BotVersion']
        self.assertEqual(bot_version, "v1.8.2")
    def test_unfilled(self):
        server_ip = GM.cfg['Connection_Settings']['ServerIP']
        self.assertEqual(server_ip, "SERVER_IP")
        user_id = GM.cfg['Connection_Settings']['UserID']
        self.assertEqual(user_id, "USERNAME")
        server_pass = GM.cfg['Connection_Settings']['ServerPassword']
        self.assertEqual(user_id, "PASSWORD")
        server_port = int(GM.cfg['Connection_Settings']['ServerPort'])
        self.assertEqual(user_id, "PORT_NUMBER")
        user_cert = GM.cfg['Connection_Settings']['UserCertification']
        self.assertEqual(user_id, "CERT_FILE_PATH")
        default_channel = GM.cfg['Connection_Settings']['DefaultChannel']
        self.assertEqual(default_channel, "DEFAULT_CHANNEL_NAME")



if __name__ == '__main__':
	unittest.main()