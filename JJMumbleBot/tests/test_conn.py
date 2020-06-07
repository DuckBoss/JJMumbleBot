from JJMumbleBot.lib.utils.dir_utils import get_main_dir
import pymumble_py3 as pymumble
from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
from JJMumbleBot.settings import global_settings
import configparser


# sys.path.append(".")
# sys.path.append(".")


class Test_Conn:
    def setup_method(self):
        # Initialize configs.
        global_settings.cfg = configparser.ConfigParser()
        global_settings.cfg.read(f"{get_main_dir()}/cfg/templates/config_template.ini")
        self.md = BotServiceHelper.retrieve_mumble_data()

    def test_connectivity(self):
        mumble_inst = pymumble.Mumble('127.0.0.1', port=64738, user='TravisCIClient',
                                      password='test')
        assert mumble_inst is not None

    def test_server_ip(self):
        server_ip = self.md.server_ip
        assert server_ip == "SERVER_IP"

    def test_user_id(self):
        user_id = self.md.user_id
        assert user_id == "USERNAME"

    def test_server_pass(self):
        server_pass = self.md.server_pass
        assert server_pass == "PASSWORD"

    def test_server_port(self):
        server_port = self.md.server_port
        assert server_port == "PORT_NUMBER"

    def test_user_cert(self):
        user_cert = self.md.user_cert
        assert user_cert == "CERT_FILE_PATH"
