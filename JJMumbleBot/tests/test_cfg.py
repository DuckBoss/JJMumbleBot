import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_main_dir
from JJMumbleBot.lib.utils.runtime_utils import get_version
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *


class Test_Cfg:
    def setup_method(self):
        # Initialize configs.
        global_settings.cfg = configparser.ConfigParser()
        global_settings.cfg.read(f"{get_main_dir()}/cfg/templates/config_template.ini")

    def test_version(self):
        bot_version = get_version()
        assert bot_version == META_VERSION

    # Connection Config Tests
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

    def test_def_comment(self):
        default_comment = global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_COMMENT]
        assert default_comment == "Hello! I am JJMumbleBot!"
    #################################

    # Web Interface Config Tests
    def test_web_intf(self):
        enable_web_interface = global_settings.cfg.getboolean(C_WEB_SETTINGS, P_USER_COMMENT)
        assert enable_web_interface is True

    def test_web_ip(self):
        web_server_ip = global_settings.cfg[C_WEB_SETTINGS][P_WEB_IP]
        assert web_server_ip == "127.0.0.1"

    def test_web_port(self):
        web_page_port = int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_PAGE_PORT])
        assert web_page_port == 7000

    def test_socket_port(self):
        web_socket_port = int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_SOCK_PORT])
        assert web_socket_port == 7001

    def test_web_tick_rate(self):
        web_tick_rate = int(global_settings.cfg[C_WEB_SETTINGS][P_WEB_TICK_RATE])
        assert web_tick_rate == 1
    #################################

    # Media Settings Config Tests
    def test_vlc_location(self):
        vlc_location = global_settings.cfg[C_MEDIA_SETTINGS][P_WEB_IP]
        assert vlc_location == "vlc"

    def test_stereo_audio(self):
        stereo_audio = global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_VLC_STEREO)
        assert stereo_audio is True

    def test_vlc_quiet(self):
        vlc_quiet = global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_VLC_QUIET)
        assert vlc_quiet is True

    def test_vlc_default_volume(self):
        vlc_default_volume = global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_DEFAULT_VOLUME]
        assert vlc_default_volume == "0.3"

    def test_vlc_duck_audio(self):
        vlc_duck_audio = global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_VLC_DUCK)
        assert vlc_duck_audio is False

    def test_vlc_duck_volume(self):
        vlc_duck_volume = global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_DUCK_VOLUME]
        assert vlc_duck_volume == "0.05"

    def test_vlc_duck_threshold(self):
        vlc_duck_threshold = global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_DUCK_THRESHOLD]
        assert vlc_duck_threshold == "2500.0"

    def test_vlc_duck_delay(self):
        vlc_duck_delay = global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_DUCK_DELAY]
        assert vlc_duck_delay == "1.0"

    def test_vlc_max_queue_length(self):
        vlc_max_queue_length = int(global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_QUEUE_LEN])
        assert vlc_max_queue_length == 50

    def test_temp_media_directory(self):
        temp_media_directory = global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]
        assert temp_media_directory == "TEMP_MEDIA_DIR_PATH"

    def test_perm_media_directory(self):
        perm_media_directory = global_settings.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]
        assert perm_media_directory == "PERM_MEDIA_DIR_PATH"
    #################################

    # Logging Config Tests
    def test_enable_logging(self):
        enable_logging = global_settings.cfg.getboolean(C_LOGGING, P_LOG_ENABLE)
        assert enable_logging is True

    def test_max_log_limit(self):
        max_log_limit = int(global_settings.cfg[C_LOGGING][P_LOG_MAX])
        assert max_log_limit == 20

    def test_hide_message_logging(self):
        hide_message_logging = global_settings.cfg.getboolean(C_LOGGING, P_LOG_MESSAGES)
        assert hide_message_logging is True

    def test_log_directory(self):
        log_directory = global_settings.cfg[C_LOGGING][P_LOG_DIR]
        assert log_directory == "LOGS_DIR_PATH"
    #################################

    # Plugin Config Tests
    def test_disabled_plugins(self):
        disabled_plugins = list(loads(global_settings.cfg.get(C_PLUGIN_SETTINGS, P_PLUG_DISABLED)))
        assert len(disabled_plugins) == 0

    def test_safe_mode_plugins(self):
        safe_mode_plugins = list(loads(global_settings.cfg.get(C_PLUGIN_SETTINGS, P_PLUG_SAFE)))
        assert len(safe_mode_plugins) == 2

    def test_allowed_root_channels_for_temp_channels(self):
        allowed_root_channels_for_temp_channels = list(loads(global_settings.cfg.get(C_PLUGIN_SETTINGS, P_PLUG_ALLOWED_CHANNELS)))
        assert len(allowed_root_channels_for_temp_channels) == 1
    #################################

    # Main Settings Config Tests
    def test_enable_database_backup(self):
        enable_database_backup = global_settings.cfg.getboolean(C_MAIN_SETTINGS, P_DB_BACKUP)
        assert enable_database_backup is True

    def test_command_tick_rate(self):
        command_tick_rate = global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TICK_RATE]
        assert command_tick_rate == "0.1"

    def test_command_multi_lim(self):
        command_multi_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_MULTI_LIM])
        assert command_multi_lim == 100

    def test_command_queue_lim(self):
        command_queue_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_QUEUE_LIM])
        assert command_queue_lim == 500

    def test_command_token(self):
        command_tick_rate = global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]
        assert command_tick_rate == "!"

    def test_command_hist_lim(self):
        command_hist_lim = int(global_settings.cfg[C_MAIN_SETTINGS][P_CMD_HIST_LIM])
        assert command_hist_lim == 25
    #################################

    # PGUI Settings Config Tests
    def test_canvas_bg_color(self):
        canvas_bg_color = global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_BG_COL]
        assert canvas_bg_color == "black"

    def test_canvas_img_color(self):
        canvas_img_color = global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_IMG_BG_COL]
        assert canvas_img_color == "black"

    def test_canvas_def_alignment(self):
        canvas_def_alignment = global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_ALGN]
        assert canvas_def_alignment == "center"

    def test_canvas_border(self):
        canvas_border = int(global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_BORD])
        assert canvas_border == 0

    def test_canvas_text_color(self):
        canvas_text_color = global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_TXT_COL]
        assert canvas_text_color == "white"

    def test_text_def_font(self):
        canvas_def_font = global_settings.cfg[C_PGUI_SETTINGS][P_TXT_DEFAULT_FONT]
        assert canvas_def_font == "Calibri"

    def test_text_header_color(self):
        text_header_color = global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]
        assert text_header_color == "red"

    def test_text_index_color(self):
        text_header_color = global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]
        assert text_header_color == "cyan"

    def test_text_sub_header_color(self):
        text_header_color = global_settings.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]
        assert text_header_color == "yellow"
    #################################
