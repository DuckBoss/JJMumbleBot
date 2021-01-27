import JJMumbleBot.core.bot_service as service
import JJMumbleBot.settings.global_settings as global_settings
from JJMumbleBot.lib.errors import SysArgError
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.resources.strings import *
import argparse
import configparser
from shutil import copy
from os import path, environ


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A plugin-based All-In-One mumble bot solution in python 3.7+ with extensive features and support "
                    "for custom plugins."
    )
    parser._action_groups.pop()
    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    # Connection launch parameters
    required_args.add_argument('-ip', dest='server_ip', required=False, default=None,
                               help='Enter the server IP using this parameter if environment variables are not being used.')
    required_args.add_argument('-port', dest='server_port', required=False, default=None,
                               help='Enter the server port using this parameter if environment variables are not being used.')
    optional_args.add_argument('-password', dest='server_password',
                               help='Enter the server password using this parameter.')
    optional_args.add_argument('-forcedefaults', dest='force_defaults', action='store_true', default=False,
                               help="Forces the bot instance to use the default config, aliases, and regenerates the internal database.")
    optional_args.add_argument('-cert', dest='server_cert', default=None,
                               help='Enter the bot client certificate path using this parameter.')
    optional_args.add_argument('-generatecert', dest='generate_cert', action='store_true', default=False,
                               help='Enables automatic .pem certificate creation for the bot client.\n'
                                    'This is useful if the server requires a certificate and the bot '
                                    'does not have a premade certificate.')
    optional_args.add_argument('-superuser', dest='super_user', default=None,
                               help='Enter the default super user for the bot client using this parameter.')
    optional_args.add_argument('-username', dest='server_username', default=None,
                               help='Enter the username of the bot using this parameter.\n'
                                    'If the bot is registered with a certificate, the username must '
                                    'match the username registered in the certificate.')
    optional_args.add_argument('-defaultchannel', dest='default_channel', default=None,
                               help='Enter the default channel the bot should join after connecting to the server.')
    optional_args.add_argument('-autoreconnect', dest='auto_reconnect', action='store_true', default=False,
                               help='Enables auto-reconnecting if the bot disconnects from the mumble server.')
    optional_args.add_argument('-selfregister', dest='self_register', action='store_true', default=False,
                               help='Enables self-registration to the connected mumble server.')
    optional_args.add_argument('-comment', dest='default_comment', default=None,
                               help='Enter the comments that are shown when users view the bot comment in a server.')

    # Web Interface Launch Parameters
    optional_args.add_argument('-useweb', dest='web_interface', action='store_true', default=False,
                               help='Enable the bot web interface with this launch parameter.')
    optional_args.add_argument('-noweb', dest='no_web_interface', action='store_true', default=False,
                               help='Disable the bot web interface with this launch parameter if it is enabled in the config.')
    optional_args.add_argument('-webip', dest='web_ip', default=None,
                               help='Enter the IP to use for the web server (if enabled).')
    optional_args.add_argument('-webport', dest='web_port', default=None,
                               help='Enter the port to use for the web server (if enabled).')
    optional_args.add_argument('-webtickrate', dest='web_tick_rate', default=None,
                               help='Enter the tick rate of the processing loop that sends data to the web interface (if enabled).')

    # Media Settings Launch Parameters
    optional_args.add_argument('-ffmpegpath', dest='ffmpeg_path', default=None,
                               help='Enter the path to ffmpeg to be used by media plugins.')
    optional_args.add_argument('-vlcpath', dest='vlc_path', default=None,
                               help='Enter the path to vlc to be used by media plugins.')
    optional_args.add_argument('-stereoaudio', dest='stereo_audio', action='store_true', default=False,
                               help='Enable stereo audio playback for the bot audio system.')
    optional_args.add_argument('-quietaudiolib', dest='quiet_audio_lib', action='store_true', default=False,
                               help='Suppress audio library console messages with this launch parameter.')
    optional_args.add_argument('-volume', dest='default_volume', default=None,
                               help='Enter the default volume to be used by the bot audio system.')
    optional_args.add_argument('-audioduck', dest='audio_duck', action='store_true', default=False,
                               help='Enable audio ducking for the bot audio system.')
    optional_args.add_argument('-audioduckvolume', dest='duck_volume', default=None,
                               help='Enter the volume to duck to when audio ducking (If audio ducking enabled).')
    optional_args.add_argument('-audioduckthreshold', dest='duck_threshold', default=None,
                               help='Enter the threshold before ducking audio (If audio ducking enabled).')
    optional_args.add_argument('-audioduckdelay', dest='duck_delay', default=None,
                               help='Enter the delay before ducking audio (If audio ducking enabled).')
    optional_args.add_argument('-maxqueuelength', dest='max_queue_length', default=None,
                               help='Enter the maximum queue length allowed for the bot audio system.')
    optional_args.add_argument('-mediaproxy', dest='media_proxy', default=None,
                               help='Enter a proxy url used for the youtube-dl library with this launch parameter.')
    optional_args.add_argument('-mediacookie', dest='media_cookie', default=None,
                               help='Enter a cookies.txt directory path used for the youtube-dl library with this launch parameter.\n'
                                    'This is useful to deal with rate limits on the bot.')
    optional_args.add_argument('-tempmediadirectory', dest='temp_media_directory', default=None,
                               help='Enter the temporary media directory path to be used by media plugins.')
    optional_args.add_argument('-permmediadirectory', dest='perm_media_directory', default=None,
                               help='Enter the permanent media directory path to be used by media plugins.')
    # Logging Launch Parameters
    optional_args.add_argument('-uselogging', dest='use_logging', action='store_true', default=False,
                               help='Enable event logging for the bot service.')
    optional_args.add_argument('-maxlogs', dest='max_logs', default=None,
                               help='Enter the maximum number of logs to be stored by the logging system.')
    optional_args.add_argument('-maxlogsize', dest='max_log_size', default=None,
                               help='Enter the maximum size of each log generated by the logging system.')
    optional_args.add_argument('-hidelogmessages', dest='hide_log_messages', action='store_true', default=False,
                               help='Hide potentially sensitive information in logs such as usernames/messages.')
    optional_args.add_argument('-logdirectory', dest='log_directory', default=None,
                               help='Enter the log directory path to be used by the bot to store logs.')
    optional_args.add_argument('-logtrace', dest='log_trace', action='store_true', default=False,
                               help='Enable stack trace logging for all logged events.')

    # Plugin launch parameters are currently unsupported.
    # If you wish to modify these properties you can edit your config.ini file.

    # Main Settings Launch Parameters
    optional_args.add_argument('-usedatabasebackups', dest='use_database_backups', action='store_true', default=False,
                               help='Enable automatic database backups for the bot service.')
    optional_args.add_argument('-cmdtickrate', dest='cmd_tick_rate', default=None,
                               help='Enter a custom tick rate for commands to be processed.')
    optional_args.add_argument('-multicmdlimit', dest='multi_cmd_limit', default=None,
                               help='Enter the maximum number of commands per multi-command input.')
    optional_args.add_argument('-cmdqueuelimit', dest='cmd_queue_limit', default=None,
                               help='Enter the maximum number of commands allowed to be processed in the queue.')
    optional_args.add_argument('-cmdtoken', dest='cmd_token', default=None,
                               help='Enter a custom command token character to identify commands in the chat (must be single character).')
    optional_args.add_argument('-cmdhistlimit', dest='cmd_hist_limit', default=None,
                               help='Enter the maximum number of commands to store in the command history.')
    # PGUI Settings Launch Parameters
    optional_args.add_argument('-canvasbgcolor', dest='canvas_bg_color', default=None,
                               help='Enter a default background color for the PGUI system.')
    optional_args.add_argument('-canvasimgbgcolor', dest='canvas_img_bg_color', default=None,
                               help='Enter a default background color for images in the PGUI system.')
    optional_args.add_argument('-canvasalign', dest='canvas_alignment', default=None,
                               help='Enter a default canvas alignment for the PGUI system.')
    optional_args.add_argument('-canvasborder', dest='canvas_border', default=None,
                               help='Enter a default canvas border size for the PGUI system.')
    optional_args.add_argument('-canvastextcolor', dest='canvas_text_color', default=None,
                               help='Enter a default text color for the PGUI system.')
    optional_args.add_argument('-canvasfont', dest='canvas_font', default=None,
                               help='Enter a default font for the PGUI system.')
    optional_args.add_argument('-canvasheadtextcolor', dest='canvas_header_text_color', default=None,
                               help='Enter a default header text color for the PGUI system.')
    optional_args.add_argument('-canvasindextextcolor', dest='canvas_index_text_color', default=None,
                               help='Enter a default index text color for the PGUI system.')
    optional_args.add_argument('-canvassubheadtextcolor', dest='canvas_subheader_text_color', default=None,
                               help='Enter a default sub-header text color for the PGUI system.')

    # Safe/Verbose/Quiet Mode launch parameters
    optional_args.add_argument('-safe', dest='safe_mode', action='store_true', default=False,
                               help='Enables safe mode for the bot service which initializes the bot with safe-mode only '
                                    'plugins.')
    optional_args.add_argument('-verbose', dest='verbose_mode', action='store_true', default=False,
                               help='Enables verbose mode which displays extensive output statements from the bot service. '
                                    'This is useful for debugging purposes.')
    optional_args.add_argument('-quiet', dest='quiet_mode', action='store_true', default=False,
                               help='Enables quiet mode which suppresses output statements from the bot service. This is '
                                    'useful for running the bot in a headless environment.')

    args = parser.parse_args()

    # Safe/Verbose/Quiet Mode launch parameter handling
    if args.quiet_mode:
        global_settings.quiet_mode = True
    if args.safe_mode:
        global_settings.safe_mode = True
    elif args.verbose_mode:
        global_settings.verbose_mode = True
    if global_settings.verbose_mode and global_settings.quiet_mode:
        raise SysArgError("It looks like both verbose mode and quiet mode are enabled.\n"
                          "Only one or the other can be used!")

    if not path.exists(f'{dir_utils.get_main_dir()}/cfg/'):
        dir_utils.make_directory(f'{dir_utils.get_main_dir()}/cfg/')

    if args.force_defaults:
        dir_utils.clear_directory(f'{dir_utils.get_main_dir()}/cfg/')

    if not path.exists(f'{dir_utils.get_main_dir()}/cfg/config.ini'):
        copy(f'{dir_utils.get_main_dir()}/templates/config_template.ini', f'{dir_utils.get_main_dir()}/cfg/config.ini')
    if not path.exists(f'{dir_utils.get_main_dir()}/cfg/global_aliases.csv'):
        copy(f'{dir_utils.get_main_dir()}/templates/aliases_template.csv', f'{dir_utils.get_main_dir()}/cfg/global_aliases.csv')
    if not path.exists(f'{dir_utils.get_main_dir()}/cfg/plugins/'):
        dir_utils.make_directory(f'{dir_utils.get_main_dir()}/cfg/plugins/')

    global_settings.cfg = configparser.ConfigParser()
    global_settings.cfg.read(f'{dir_utils.get_main_dir()}/cfg/config.ini')
    global_settings.web_cfg = configparser.ConfigParser()
    if path.exists(f'{dir_utils.get_core_plugin_dir()}/web_server/metadata.ini'):
        global_settings.web_cfg.read(f'{dir_utils.get_core_plugin_dir()}/web_server/metadata.ini')

    # Overwrite connection settings if the launch parameter is provided.
    if args.server_username:
        global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID] = args.server_username

    if args.generate_cert:
        from subprocess import call
        if not path.exists('/app/JJMumbleBot/cfg/jjmumblebot.pem'):
            call(['openssl', 'req', '-x509', '-nodes', '-days', '3650',
              '-newkey', 'rsa:2048', '-keyout', '/app/JJMumbleBot/cfg/jjmumblebot.pem',
              '-out', '/app/JJMumbleBot/cfg/jjmumblebot.pem', '-subj',
              f'/CN={global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID]}'])
            global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_CERT] = f'{dir_utils.get_main_dir()}/cfg/jjmumblebot.pem'
    if args.server_cert:
        global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_CERT] = args.server_cert
    if args.auto_reconnect:
        global_settings.cfg[C_CONNECTION_SETTINGS][P_SERVER_RECONNECT] = args.auto_reconnect
    if args.default_channel:
        global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_CHANNEL] = args.default_channel
    if args.self_register:
        global_settings.cfg[C_CONNECTION_SETTINGS][P_SELF_REGISTER] = args.self_register
    if args.super_user:
        global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU] = args.super_user
    if args.default_comment:
        global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_COMMENT] = args.default_comment

    # Overwrite web settings if the launch parameter is provided.
    if args.web_interface:
        if global_settings.web_cfg:
            from JJMumbleBot.plugins.core.web_server.resources.strings import P_WEB_ENABLE
            global_settings.web_cfg[C_PLUGIN_SET][P_WEB_ENABLE] = "True"
    if args.no_web_interface:
        if global_settings.web_cfg:
            from JJMumbleBot.plugins.core.web_server.resources.strings import P_WEB_ENABLE
            global_settings.web_cfg[C_PLUGIN_SET][P_WEB_ENABLE] = "False"
    if args.web_ip:
        if global_settings.web_cfg:
            from JJMumbleBot.plugins.core.web_server.resources.strings import P_WEB_IP
            global_settings.web_cfg[C_PLUGIN_SET][P_WEB_IP] = args.web_ip
    if args.web_port:
        if global_settings.web_cfg:
            from JJMumbleBot.plugins.core.web_server.resources.strings import P_WEB_PORT
            global_settings.web_cfg[C_PLUGIN_SET][P_WEB_PORT] = args.web_port
    if args.web_tick_rate:
        if global_settings.web_cfg:
            from JJMumbleBot.plugins.core.web_server.resources.strings import P_WEB_TICK_RATE
            global_settings.web_cfg[C_PLUGIN_SET][P_WEB_TICK_RATE] = args.web_tick_rate

    # Overwrite media settings if the launch parameter is provided.
    if args.ffmpeg_path:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_FFMPEG_PATH] = args.ffmpeg_path
    if args.vlc_path:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PATH] = args.vlc_path
    if args.stereo_audio:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_USE_STEREO] = args.stereo_audio
    if args.quiet_audio_lib:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_AUDIO_LIB_QUIET] = args.quiet_audio_lib
    if args.default_volume:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_DEFAULT_VOLUME] = args.default_volume
    if args.audio_duck:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_DUCK_AUDIO] = args.audio_duck
    if args.duck_volume:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_DUCK_VOLUME] = args.duck_volume
    if args.duck_threshold:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_DUCK_THRESHOLD] = args.duck_threshold
    if args.duck_delay:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_DUCK_DELAY] = args.duck_delay
    if args.max_queue_length:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_QUEUE_LEN] = args.max_queue_length
    if args.media_proxy:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_PROXY_URL] = args.media_proxy
    if args.media_cookie:
        global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE] = args.media_cookie
    if args.temp_media_directory:
        global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR] = args.temp_media_directory
    if args.temp_media_directory:
        global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR] = args.temp_media_directory
    # Overwrite logging settings if the launch parameter is provided.
    if args.use_logging:
        global_settings.cfg[C_LOGGING][P_LOG_ENABLE] = args.use_logging
    if args.max_logs:
        global_settings.cfg[C_LOGGING][P_LOG_MAX] = args.max_logs
    if args.max_log_size:
        global_settings.cfg[C_LOGGING][P_LOG_SIZE_MAX] = args.max_log_size
    if args.hide_log_messages:
        global_settings.cfg[C_LOGGING][P_LOG_MESSAGES] = args.hide_log_messages
    if args.log_directory:
        global_settings.cfg[C_LOGGING][P_LOG_DIR] = args.log_directory
    if args.log_trace:
        global_settings.cfg[C_LOGGING][P_LOG_TRACE] = args.log_trace
    # Overwrite main settings if the launch parameter is provided.
    if args.use_database_backups:
        global_settings.cfg[C_MAIN_SETTINGS][P_DB_BACKUP] = args.use_database_backups
    if args.cmd_tick_rate:
        global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TICK_RATE] = args.cmd_tick_rate
    if args.multi_cmd_limit:
        global_settings.cfg[C_MAIN_SETTINGS][P_CMD_MULTI_LIM] = args.multi_cmd_limit
    if args.cmd_queue_limit:
        global_settings.cfg[C_MAIN_SETTINGS][P_CMD_QUEUE_LIM] = args.cmd_queue_limit
    if args.cmd_token:
        global_settings.cfg[C_MAIN_SETTINGS][P_CMD_TOKEN] = args.cmd_token
    if args.cmd_hist_limit:
        global_settings.cfg[C_MAIN_SETTINGS][P_CMD_HIST_LIM] = args.cmd_hist_limit
    # Overwrite pgui settings if the launch parameter is provided.
    if args.canvas_bg_color:
        global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_BG_COL] = args.canvas_bg_color
    if args.canvas_img_bg_color:
        global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_IMG_BG_COL] = args.canvas_img_bg_color
    if args.canvas_alignment:
        global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_ALGN] = args.canvas_alignment
    if args.canvas_border:
        global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_BORD] = args.canvas_border
    if args.canvas_text_color:
        global_settings.cfg[C_PGUI_SETTINGS][P_CANVAS_TXT_COL] = args.canvas_text_color
    if args.canvas_font:
        global_settings.cfg[C_PGUI_SETTINGS][P_TXT_DEFAULT_FONT] = args.canvas_font
    if args.canvas_header_text_color:
        global_settings.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL] = args.canvas_header_text_color
    if args.canvas_index_text_color:
        global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL] = args.canvas_index_text_color
    if args.canvas_subheader_text_color:
        global_settings.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL] = args.canvas_subheader_text_color

    # Set the IP, port and password from the environment variables if not passed using options
    if args.server_ip is None:
        server_ip = environ.get(ENV_MUMBLE_IP)
        if server_ip is None:
            server_ip = '127.0.0.1'
    else:
        server_ip = args.server_ip

    if args.server_port is None:
        server_port = environ.get(ENV_MUMBLE_PORT)
        if server_port is None:
            server_port = '64738'
    else:
        server_port = args.server_port

    if args.server_password is None:
        server_password = environ.get(ENV_MUMBLE_PASSWORD)
        if server_password is None:
            server_password = ''
    else:
        server_password = args.server_password

    # Initialize bot service.
    service.BotService(server_ip, int(server_port), server_password)
