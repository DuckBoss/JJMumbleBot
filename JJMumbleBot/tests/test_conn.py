import pymumble_py3 as pymumble
import configparser
from JJMumbleBot.lib.utils.dir_utils import get_main_dir
from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
from JJMumbleBot.settings import global_settings


class TestBasicConnectivity:
    def setup_method(self):
        # Initialize configs.
        global_settings.cfg = configparser.ConfigParser()
        global_settings.cfg.read(f"{get_main_dir()}/tests/dummy_config.ini")
        self.md = BotServiceHelper.retrieve_mumble_data('0.0.0.0', 64738, 'test')

    def test_connectivity(self):
        mumble_inst = pymumble.Mumble(self.md.ip_address, port=self.md.port, user=self.md.user_id,
                                           password=self.md.password, stereo=self.md.stereo)
        assert mumble_inst is not None

    def test_server_ip(self):
        assert self.md.ip_address == "0.0.0.0"

    def test_user_id(self):
        assert self.md.user_id == "TravisCIClient"

    def test_server_pass(self):
        assert self.md.password == "test"

    def test_server_port(self):
        assert self.md.port == 64738

    def test_user_cert(self):
        assert self.md.certificate == "test_cert"

    def test_stereo(self):
        assert self.md.stereo is True
