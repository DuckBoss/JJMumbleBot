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
        self.assertEqual(bot_version, "v1.8.4")
    def test_server_ip(self):
        server_ip = GM.cfg['Connection_Settings']['ServerIP']
        self.assertEqual(server_ip, "SERVER_IP")
    def test_user_id(self):
        user_id = GM.cfg['Connection_Settings']['UserID']
        self.assertEqual(user_id, "USERNAME")
    def test_server_pass(self):
        server_pass = GM.cfg['Connection_Settings']['ServerPassword']
        self.assertEqual(server_pass, "PASSWORD")
    def test_server_port(self):
        server_port = GM.cfg['Connection_Settings']['ServerPort']
        self.assertEqual(server_port, "PORT_NUMBER")
    def test_user_cert(self):
        user_cert = GM.cfg['Connection_Settings']['UserCertification']
        self.assertEqual(user_cert, "CERT_FILE_PATH")
    def test_def_channel(self):
        default_channel = GM.cfg['Connection_Settings']['DefaultChannel']
        self.assertEqual(default_channel, "DEFAULT_CHANNEL_NAME")



if __name__ == '__main__':
	unittest.main()