import configparser
from json import loads
from JJMumbleBot.lib.utils.dir_utils import get_main_dir
from JJMumbleBot.lib.utils.runtime_utils import get_version
from JJMumbleBot.lib.resources.strings import *


class TestConfigTemplate:
    def setup_method(self):
        # Initialize configs.
        self.cfg = configparser.ConfigParser()
        self.cfg.read(f"{get_main_dir()}/templates/config_template.ini")

    def test_version(self):
        bot_version = get_version()
        assert bot_version == META_VERSION

    # Connection Config Tests
    def test_user_id(self):
        user_id = self.cfg[C_CONNECTION_SETTINGS][P_USER_ID]
        assert user_id == "JJMumbleBot"

    def test_user_cert(self):
        user_cert = self.cfg[C_CONNECTION_SETTINGS][P_USER_CERT]
        assert user_cert == ""

    def test_def_channel(self):
        default_channel = self.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_CHANNEL]
        assert default_channel == "Root"

    def test_super_user(self):
        super_user = self.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU]
        assert super_user == ""

    def test_self_register(self):
        self_register = self.cfg.getboolean(C_CONNECTION_SETTINGS, P_SELF_REGISTER)
        assert self_register is False

    def test_auto_reconnect(self):
        auto_reconnect = self.cfg.getboolean(C_CONNECTION_SETTINGS, P_SERVER_RECONNECT)
        assert auto_reconnect is False

    def test_def_comment(self):
        default_comment = self.cfg[C_CONNECTION_SETTINGS][P_USER_COMMENT]
        assert default_comment == "Hello! I am JJMumbleBot!"
    #################################

    # Media Settings Config Tests
    def test_ffmpeg_location(self):
        vlc_location = self.cfg[C_MEDIA_SETTINGS][P_MEDIA_FFMPEG_PATH]
        assert vlc_location == "ffmpeg"

    def test_vlc_location(self):
        vlc_location = self.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PATH]
        assert vlc_location == "vlc"

    def test_stereo_audio(self):
        stereo_audio = self.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_USE_STEREO)
        assert stereo_audio is True

    def test_audio_library_quiet(self):
        audio_library_quiet = self.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_AUDIO_LIB_QUIET)
        assert audio_library_quiet is True

    def test_media_default_volume(self):
        media_default_volume = self.cfg[C_MEDIA_SETTINGS][P_MEDIA_DEFAULT_VOLUME]
        assert media_default_volume == "0.3"

    def test_media_duck_audio(self):
        media_duck_audio = self.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_DUCK_AUDIO)
        assert media_duck_audio is False

    def test_media_duck_volume(self):
        media_duck_volume = self.cfg[C_MEDIA_SETTINGS][P_MEDIA_DUCK_VOLUME]
        assert media_duck_volume == "0.05"

    def test_media_duck_threshold(self):
        media_duck_threshold = self.cfg[C_MEDIA_SETTINGS][P_MEDIA_DUCK_THRESHOLD]
        assert media_duck_threshold == "2500.0"

    def test_media_duck_delay(self):
        media_duck_delay = self.cfg[C_MEDIA_SETTINGS][P_MEDIA_DUCK_DELAY]
        assert media_duck_delay == "1.0"

    def test_media_max_queue_length(self):
        media_max_queue_length = int(self.cfg[C_MEDIA_SETTINGS][P_MEDIA_QUEUE_LEN])
        assert media_max_queue_length == 50

    def test_media_proxy(self):
        media_proxy = self.cfg[C_MEDIA_SETTINGS][P_MEDIA_PROXY_URL]
        assert media_proxy == ""

    def test_media_cookie(self):
        media_cookie = self.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE]
        assert media_cookie == ""

    def test_temp_media_directory(self):
        temp_media_directory = self.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]
        assert temp_media_directory == ""

    def test_perm_media_directory(self):
        perm_media_directory = self.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]
        assert perm_media_directory == ""
    #################################

    # Logging Config Tests
    def test_enable_logging(self):
        enable_logging = self.cfg.getboolean(C_LOGGING, P_LOG_ENABLE)
        assert enable_logging is False

    def test_max_log_limit(self):
        max_log_limit = int(self.cfg[C_LOGGING][P_LOG_MAX])
        assert max_log_limit == 20

    def test_max_log_size(self):
        max_log_size = int(self.cfg[C_LOGGING][P_LOG_SIZE_MAX])
        assert max_log_size == 1500000

    def test_hide_message_logging(self):
        hide_message_logging = self.cfg.getboolean(C_LOGGING, P_LOG_MESSAGES)
        assert hide_message_logging is True

    def test_log_directory(self):
        log_directory = self.cfg[C_LOGGING][P_LOG_DIR]
        assert log_directory == ""

    def test_enable_log_stack_trace(self):
        hide_message_logging = self.cfg.getboolean(C_LOGGING, P_LOG_TRACE)
        assert hide_message_logging is False
    #################################

    # Plugin Config Tests
    def test_disabled_plugins(self):
        disabled_plugins = list(loads(self.cfg.get(C_PLUGIN_SETTINGS, P_PLUG_DISABLED)))
        assert len(disabled_plugins) == 0

    def test_safe_mode_plugins(self):
        safe_mode_plugins = list(loads(self.cfg.get(C_PLUGIN_SETTINGS, P_PLUG_SAFE)))
        assert len(safe_mode_plugins) == 2

    def test_allowed_root_channels_for_temp_channels(self):
        allowed_root_channels_for_temp_channels = list(loads(self.cfg.get(C_PLUGIN_SETTINGS, P_PLUG_ALLOWED_CHANNELS)))
        assert len(allowed_root_channels_for_temp_channels) == 1
    #################################

    # Main Settings Config Tests
    def test_enable_database_integrity_check(self):
        enable_database_integrity_check = self.cfg.getboolean(C_MAIN_SETTINGS, P_DB_INTEGRITY)
        assert enable_database_integrity_check is True

    def test_enable_database_backup(self):
        enable_database_backup = self.cfg.getboolean(C_MAIN_SETTINGS, P_DB_BACKUP)
        assert enable_database_backup is False

    def test_command_tick_rate(self):
        command_tick_rate = self.cfg[C_MAIN_SETTINGS][P_CMD_TICK_RATE]
        assert command_tick_rate == "0.1"

    def test_command_multi_lim(self):
        command_multi_lim = int(self.cfg[C_MAIN_SETTINGS][P_CMD_MULTI_LIM])
        assert command_multi_lim == 200

    def test_command_queue_lim(self):
        command_queue_lim = int(self.cfg[C_MAIN_SETTINGS][P_CMD_QUEUE_LIM])
        assert command_queue_lim == 600

    def test_command_token(self):
        command_tick_rate = self.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN]
        assert command_tick_rate == "!"

    def test_command_hist_lim(self):
        command_hist_lim = int(self.cfg[C_MAIN_SETTINGS][P_CMD_HIST_LIM])
        assert command_hist_lim == 25
    #################################

    # PGUI Settings Config Tests
    def test_canvas_bg_color(self):
        canvas_bg_color = self.cfg[C_PGUI_SETTINGS][P_CANVAS_BG_COL]
        assert canvas_bg_color == "black"

    def test_canvas_img_color(self):
        canvas_img_color = self.cfg[C_PGUI_SETTINGS][P_CANVAS_IMG_BG_COL]
        assert canvas_img_color == "black"

    def test_canvas_def_alignment(self):
        canvas_def_alignment = self.cfg[C_PGUI_SETTINGS][P_CANVAS_ALGN]
        assert canvas_def_alignment == "center"

    def test_canvas_border(self):
        canvas_border = int(self.cfg[C_PGUI_SETTINGS][P_CANVAS_BORD])
        assert canvas_border == 0

    def test_canvas_text_color(self):
        canvas_text_color = self.cfg[C_PGUI_SETTINGS][P_CANVAS_TXT_COL]
        assert canvas_text_color == "Snow"

    def test_text_def_font(self):
        canvas_def_font = self.cfg[C_PGUI_SETTINGS][P_TXT_DEFAULT_FONT]
        assert canvas_def_font == "Georgia"

    def test_text_header_color(self):
        text_header_color = self.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]
        assert text_header_color == "red"

    def test_text_index_color(self):
        text_header_color = self.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]
        assert text_header_color == "cyan"

    def test_text_sub_header_color(self):
        text_header_color = self.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]
        assert text_header_color == "yellow"
    #################################
