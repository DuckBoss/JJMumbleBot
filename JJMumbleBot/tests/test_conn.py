from JJMumbleBot.lib.utils.dir_utils import get_main_dir
from JJMumbleBot.lib.pymumble import pymumble_py3 as pymumble
from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
from JJMumbleBot.settings import global_settings
import configparser
import unittest


# sys.path.append(".")
# sys.path.append(".")


class Tests(unittest.TestCase):
    md = None

    def setUp(self):
        global md
        # Initialize configs.
        global_settings.cfg = configparser.ConfigParser()
        global_settings.cfg.read(f"{get_main_dir()}/cfg/templates/config_template.ini")
        md = BotServiceHelper.retrieve_mumble_data()

    def test_connectivity(self):
        mumble_inst = pymumble.Mumble('127.0.0.1', port=64738, user='TravisCIClient',
                                      password='test')
        self.assertEqual(mumble_inst, not None)

    def test_server_ip(self):
        server_ip = md.server_ip
        self.assertEqual(server_ip, "SERVER_IP")

    def test_user_id(self):
        user_id = md.user_id
        self.assertEqual(user_id, "USERNAME")

    def test_server_pass(self):
        server_pass = md.server_pass
        self.assertEqual(server_pass, "PASSWORD")

    def test_server_port(self):
        server_port = md.server_port
        self.assertEqual(server_port, "PORT_NUMBER")

    def test_user_cert(self):
        user_cert = md.user_cert
        self.assertEqual(user_cert, "CERT_FILE_PATH")


if __name__ == '__main__':
    unittest.main()
