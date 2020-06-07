from JJMumbleBot.lib.utils.dir_utils import get_main_dir
from JJMumbleBot.lib.utils.runtime_utils import get_version
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
import configparser


# sys.path.append(".")
# sys.path.append(".")


class Test_Cfg:
    def setup_method(self):
        # Initialize configs.
        global_settings.cfg = configparser.ConfigParser()
        global_settings.cfg.read(f"{get_main_dir()}/cfg/templates/config_template.ini")

    def test_version(self):
        bot_version = get_version()
        assert bot_version == META_VERSION

    def test_server_ip(self):
        server_ip = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_IP]
        assert server_ip == "SERVER_IP"

    def test_user_id(self):
        user_id = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID]
        assert user_id == "USERNAME"

    def test_server_pass(self):
        server_pass = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_PASS]
        assert server_pass == "PASSWORD"

    def test_server_port(self):
        server_port = global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_PORT]
        assert server_port == "PORT_NUMBER"

    def test_user_cert(self):
        user_cert = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_CERT]
        assert user_cert == "CERT_FILE_PATH"

    def test_def_channel(self):
        default_channel = global_settings.cfg[C_CONNECTION_SETTINGS][P_CHANNEL_DEF]
        assert default_channel == "DEFAULT_CHANNEL_NAME"

    def test_super_user(self):
        super_user = global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU]
        assert super_user == "DEFAULT_SUPER_USER_NAME"

    def test_self_register(self):
        self_register = global_settings.cfg.getboolean(C_CONNECTION_SETTINGS, P_SELF_REGISTER)
        assert self_register is True
