from JJMumbleBot.lib.utils.dir_utils import get_main_dir
from JJMumbleBot.lib.utils.runtime_utils import get_version
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
import configparser
import unittest
# sys.path.append(".")
# sys.path.append(".")


class Tests(unittest.TestCase):
    def setUp(self):
        # Initialize configs.
        global_settings.cfg = configparser.ConfigParser()
        global_settings.cfg.read(f"{get_main_dir()}/cfg/templates/config_template.ini")

    def test_version(self):
        bot_version = get_version()
        self.assertEqual(bot_version, META_VERSION)

    def test_server_ip(self):
        server_ip = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_IP]
        self.assertEqual(server_ip, "SERVER_IP")

    def test_user_id(self):
        user_id = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID]
        self.assertEqual(user_id, "USERNAME")

    def test_server_pass(self):
        server_pass = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_PASS]
        self.assertEqual(server_pass, "PASSWORD")

    def test_server_port(self):
        server_port = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_PORT]
        self.assertEqual(server_port, "PORT_NUMBER")

    def test_user_cert(self):
        user_cert = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_CERT]
        self.assertEqual(user_cert, "CERT_FILE_PATH")

    def test_def_channel(self):
        default_channel = global_settings.cfg[C_CONNECTION_SETTINGS][P_CHANNEL_DEF]
        self.assertEqual(default_channel, "DEFAULT_CHANNEL_NAME")


if __name__ == '__main__':
    unittest.main()
