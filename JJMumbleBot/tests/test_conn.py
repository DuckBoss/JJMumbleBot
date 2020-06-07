import pymumble_py3 as pymumble
import sys
import configparser


from JJMumbleBot.lib.utils.dir_utils import get_main_dir
from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
from JJMumbleBot.settings import global_settings


class Test_Conn:
    def setup_method(self):
        # Initialize configs.
        global_settings.cfg = configparser.ConfigParser()
        global_settings.cfg.read(f"{get_main_dir()}/tests/dummy_config.ini")
        self.md = BotServiceHelper.retrieve_mumble_data()

    def test_connectivity(self):
        mumble_inst = pymumble.Mumble(self.md.ip_address, port=self.md.port, user=self.md.user_id,
                                      password=self.md.password)
        assert mumble_inst is not None

    def test_server_ip(self):
        server_ip = self.md.server_ip
        assert server_ip == "127.0.0.1"

    def test_user_id(self):
        user_id = self.md.user_id
        assert user_id == "TravisCIClient"

    def test_server_pass(self):
        server_pass = self.md.server_pass
        assert server_pass == "test"

    def test_server_port(self):
        server_port = self.md.server_port
        assert server_port == 64738

    def test_user_cert(self):
        user_cert = self.md.user_cert
        assert user_cert == "test_cert"
