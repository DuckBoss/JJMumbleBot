from JJMumbleBot.settings import global_settings
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.errors import ExitCodes
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.resources.strings import *
from pymumble_py3 import errors
from os import path
from json import loads, dumps
from datetime import datetime
import configparser


def parse_message(text):
    message = text.message.strip()
    user = global_settings.mumble_inst.users[text.actor]

    if message[0] == runtime_settings.cmd_token:
        log(INFO, f"Commands Received: [{user['name']} -> {message}]", origin=L_COMMAND, print_mode=PrintMode.REG_PRINT.value)
        # example all_commands input: !version ; !about ; !yt twice ; !p ; !status
        all_commands = [msg.strip() for msg in message.split(';')]
        # example all_commands output: ["!version", "!about", "!yt twice", "!p", "!status"]

        # add to command history
        for cmd in all_commands:
            global_settings.cmd_history.insert(cmd)
        if len(all_commands) > runtime_settings.multi_cmd_limit:
            log(WARNING,
                f"The multi-command limit was reached! The multi-command limit is {runtime_settings.multi_cmd_limit} commands per line.",
                origin=L_COMMAND,
                print_mode=PrintMode.REG_PRINT.value)
            return
        return all_commands

    if "<img" in message:
        log(INFO, f"Message Received: [{user['name']} -> Image Data]", print_mode=PrintMode.REG_PRINT.value)
    elif "<a href=" in message:
        log(INFO, f"Message Received: [{user['name']} -> Hyperlink Data]", print_mode=PrintMode.REG_PRINT.value)
    else:
        if global_settings.cfg.getboolean(C_LOGGING, P_LOG_MESSAGES, fallback=True):
            log(INFO, f"Message Received: [{user['name']} -> #####]", print_mode=PrintMode.REG_PRINT.value)
        else:
            log(INFO, f"Message Received: [{user['name']} -> {message}]", print_mode=PrintMode.REG_PRINT.value)
    return None


def deafen(username):
    user = get_user(username)
    if user:
        if not user.get("deaf", False):
            log(INFO, f"Deafening user:[{user['name']}]", origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value)
            user.deafen()
            return True
    return False


def undeafen(username):
    user = get_user(username)
    if user:
        if user.get("deaf", False):
            log(INFO, f"Undeafening user:[{user['name']}]", origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value)
            user.undeafen()
            return True
    return False


def mute(username: str = None):
    if username:
        user = get_user(username)
        if user:
            if not user.get("mute", False):
                log(INFO, f"Muting user:[{user['name']}]", origin=L_COMMAND,
                    print_mode=PrintMode.VERBOSE_PRINT.value)
                user.mute()
                return True
        return False
    else:
        if runtime_settings.muted:
            return False
        global_settings.mumble_inst.users.myself.mute()
        runtime_settings.muted = True
        return True


def unmute(username: str = None):
    if username:
        user = get_user(username)
        if user:
            if user.get("mute", False):
                log(INFO, f"Unmuting user:[{user['name']}]", origin=L_COMMAND,
                    print_mode=PrintMode.VERBOSE_PRINT.value)
                user.unmute()
                return True
        return False
    else:
        if not runtime_settings.muted:
            return False
        global_settings.mumble_inst.users.myself.unmute()
        runtime_settings.muted = False
        return True


def echo(channel, message_text, ignore_whisper=False):
    if channel is None:
        return
    if runtime_settings.whisper_target is not None and not ignore_whisper:
        if runtime_settings.whisper_target["type"] == 0:
            global_settings.mumble_inst.channels[runtime_settings.whisper_target["id"]].send_text_message(message_text)
        elif runtime_settings.whisper_target["type"] == 1:
            msg_id(runtime_settings.whisper_target["id"], message_text)
        elif runtime_settings.whisper_target["type"] == 2:
            for person in runtime_settings.whisper_target["id"]:
                msg_id(person, message_text)
        return
    channel.send_text_message(message_text)


def set_whisper_user(username):
    for user in global_settings.mumble_inst.users:
        if global_settings.mumble_inst.users[user]['name'] == username:
            runtime_settings.whisper_target = {"id": global_settings.mumble_inst.users[user]['session'], "type": 1}
            global_settings.mumble_inst.sound_output.set_whisper(runtime_settings.whisper_target["id"], channel=False)
            return True
    return False


def set_whisper_multi_user(users_list):
    if not isinstance(users_list, list):
        return
    whisper_targets = []
    for user in global_settings.mumble_inst.users:
        if global_settings.mumble_inst.users[user]['name'] in users_list:
            whisper_targets.append(global_settings.mumble_inst.users[user]['session'])
    if len(whisper_targets) < 1:
        return
    runtime_settings.whisper_target = {"id": whisper_targets, "type": 2}
    global_settings.mumble_inst.sound_output.set_whisper(runtime_settings.whisper_target["id"], channel=False)


def set_whisper_channel(channel_name):
    try:
        channel_id = get_channel(channel_name)['channel_id']
        runtime_settings.whisper_target = {"id": channel_id, "type": 0}
        global_settings.mumble_inst.sound_output.set_whisper(runtime_settings.whisper_target["id"], channel=True)
        return True
    except errors.UnknownChannelError:
        return False


def get_whisper_clients_by_type(wh_type: int):
    if runtime_settings.whisper_target is None:
        return None
    if wh_type == 0:
        return global_settings.mumble_inst.channels[runtime_settings.whisper_target['id']]['name']
    if wh_type == 1:
        for user in global_settings.mumble_inst.users:
            if global_settings.mumble_inst.users[user]['session'] == runtime_settings.whisper_target['id']:
                return global_settings.mumble_inst.users[user]['name']
    else:
        user_list = []
        for user in global_settings.mumble_inst.users:
            if global_settings.mumble_inst.users[user]['session'] == runtime_settings.whisper_target['id']:
                user_list.append(global_settings.mumble_inst.users[user]['name'])
        return user_list


def clear_whisper():
    runtime_settings.whisper_target = None
    global_settings.mumble_inst.sound_output.remove_whisper()


def kick_user(receiver, reason='N/A'):
    user = get_user(receiver)
    if user:
        log(INFO, f"Kicking user:[{user['name']}]->[{reason}]", origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value)
        user.kick(reason=reason)


def ban_user(receiver, reason='N/A'):
    user = get_user(receiver)
    if user:
        log(INFO,
            f"Banning user:[{user['name']}]->[{reason}]", origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value)
        user.ban(reason=reason)


def move_user(receiver: str, new_channel_name: str):
    channel = get_channel(new_channel_name)
    if channel:
        user = get_user(receiver)
        if user:
            log(INFO,
                f"Moving user:[{user['name']}]->[{new_channel_name}]",
                origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value)
            channel.move_in(session=user['session'])


def msg(receiver: str, message: str):
    user = get_user(receiver)
    if user:
        user.send_text_message(message)


def msg_id(receiver_id: str, message: str):
    for user in global_settings.mumble_inst.users:
        if global_settings.mumble_inst.users[user]['session'] == receiver_id:
            global_settings.mumble_inst.users[user].send_text_message(message)


def get_command_history():
    return global_settings.cmd_history.queue_storage


def clear_command_history():
    global_settings.cmd_history.clear()


def get_command_token():
    return runtime_settings.cmd_token


def get_bot_name():
    return global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID]


def get_bot_internal_name():
    return META_NAME


def get_user(username: str):
    for user in global_settings.mumble_inst.users:
        if global_settings.mumble_inst.users[user]['name'] == username:
            return global_settings.mumble_inst.users[user]
    return None


def get_user_channel(username: str):
    all_users = get_all_users()
    for user_id in get_all_users():
        if all_users[user_id]['name'] == username:
            return global_settings.mumble_inst.channels[all_users[user_id]['channel_id']]
    return None


def rename_channel(cur_channel_name: str, new_channel_name: str):
    channel = get_channel(cur_channel_name)
    if channel:
        channel.rename_channel(new_channel_name)


def move_to_channel(channel_name: str):
    channel_search = get_channel(channel_name)
    if channel_search:
        channel_search.move_in()


def get_channel(channel_name: str):
    try:
        return global_settings.mumble_inst.channels.find_by_name(channel_name)
    except errors.UnknownChannelError:
        return None


def get_default_channel():
    return global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_CHANNEL]


def get_my_channel():
    return global_settings.mumble_inst.channels[global_settings.mumble_inst.users.myself['channel_id']]


def get_all_users():
    return global_settings.mumble_inst.users


def get_all_channels():
    return global_settings.mumble_inst.channels


def get_users_in_channel(channel_name):
    return global_settings.mumble_inst.channels.find_by_name(channel_name).get_users()


def get_version():
    return META_VERSION


def get_about():
    return '<br> A plugin-based All-In-One mumble bot solution in python 3.7+ with extensive features and support for ' \
           'custom plugins.<br><a href="https://github.com/DuckBoss/JJMumbleBot">https://github.com/DuckBoss' \
           '/JJMumbleBot</a><br> '


def get_comment():
    return global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_COMMENT]


def get_users_in_my_channel():
    cur_channel = get_my_channel()
    if cur_channel:
        users = cur_channel.get_users()
        return users
    return None


def make_channel(root_channel, channel_name, temporary=False):
    allowed_channels = loads(global_settings.cfg[C_PLUGIN_SETTINGS][P_PLUG_ALLOWED_CHANNELS])
    if allowed_channels is not None:
        for chan_name in allowed_channels:
            found_channel = global_settings.mumble_inst.channels.find_by_name(chan_name)
            if found_channel is not None and found_channel.get_id() == root_channel.get_id():
                return global_settings.mumble_inst.channels.new_channel(root_channel.get_id(), channel_name, temporary=temporary)
    return None


def leave_channel():
    default_channel = get_channel(global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_CHANNEL])
    if default_channel:
        default_channel.move_in()


def remove_current_channel():
    cur_channel = get_my_channel()
    if cur_channel:
        cur_channel.remove()


def remove_channel(channel_name: str):
    channel = get_channel(channel_name)
    if channel:
        channel.remove()


def check_up_time() -> str:
    cur_time = datetime.now() - runtime_settings.start_time
    if cur_time:
        return f"{str(cur_time)[:-7]}"
    return ""


def validate_url(url: str) -> bool:
    from requests import get, exceptions
    try:
        resp = get(url)
        if resp:
            return True
    except exceptions.ConnectionError:
        return False
    return False


def validate_csv(file_path: str, field_names) -> bool:
    from csv import DictReader, Error
    try:
        with open(file_path, 'rb') as csv_handle:
            csvr = DictReader(csv_handle)
            columns = []
            for i, row in enumerate(csvr):
                columns.append(row)
                break
            for field in field_names:
                if field not in columns[0]:
                    return False
        return True
    except FileNotFoundError:
        return False
    except KeyError:
        return False
    except Error:
        return False


def validate_cfg(cfg_path: str, template_path: str) -> bool:
    options_results = []
    detected_options_count = 0
    try:
        cur_cfg = configparser.ConfigParser()
        cur_cfg.read(cfg_path)
        template_cfg = configparser.ConfigParser()
        template_cfg.read(template_path)
        for section in template_cfg.sections():
            for (option, value) in template_cfg.items(section):
                options_results.append(cur_cfg.has_option(section, option))
        for section in cur_cfg.sections():
            for _ in cur_cfg.items(section):
                detected_options_count += 1
        # Extra options detected in current config file, invalidate the config.
        if len(options_results) != detected_options_count:
            log(ERROR,
                f"Detected more options than allowed while trying to validate the current config.ini file!\n"
                f"Please make sure your config.ini file does not "
                f"have extra options compared to the template_config.ini file!",
                origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
            return False
    except configparser.Error as e:
        log(ERROR, f"Encountered a critical error while trying to validate the current config.ini file!\n{e.message}",
            origin=L_STARTUP, print_mode=PrintMode.REG_PRINT.value)
        return False
    # Validate the config if all the options match the template.
    if all(option for option in options_results):
        log(INFO, f"Successfully validated the current config.ini file.",
            origin=L_STARTUP, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    return False


def get_plugin_metadata(plugin_name: str) -> dict:
    if path.exists(f"{dir_utils.get_main_dir()}/plugins/core/{plugin_name}"):
        plugin_path = f"{dir_utils.get_main_dir()}/plugins/core/{plugin_name}"
    elif path.exists(f"{dir_utils.get_main_dir()}/plugins/extensions/{plugin_name}"):
        plugin_path = f"{dir_utils.get_main_dir()}/plugins/extensions/{plugin_name}"
    else:
        return {}

    plugin_metadata = {}
    cfg = configparser.ConfigParser()
    try:
        cfg.read(f'{plugin_path}/metadata.ini')
    except configparser.Error as e:
        log(ERROR, f"Encountered an error while parsing {plugin_name} metadata file: {e}",
            origin=L_GENERAL, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
        return {}

    plugin_metadata = dict(cfg)
    if "DEFAULT" in plugin_metadata:
        del plugin_metadata["DEFAULT"]
    plugin_metadata[C_PLUGIN_INFO][P_PLUGIN_CMDS] = dumps(list(loads(cfg.get(C_PLUGIN_INFO, P_PLUGIN_CMDS, fallback={}))))
    return plugin_metadata


def set_plugin_metadata(plugin_name: str, metadata) -> bool:
    if path.exists(f"{dir_utils.get_main_dir()}/plugins/core/{plugin_name}"):
        plugin_path = f"{dir_utils.get_main_dir()}/plugins/core/{plugin_name}"
    elif path.exists(f"{dir_utils.get_main_dir()}/plugins/extensions/{plugin_name}"):
        plugin_path = f"{dir_utils.get_main_dir()}/plugins/extensions/{plugin_name}"
    else:
        return False

    if "DEFAULT" in metadata:
        del metadata["DEFAULT"]

    cfg = configparser.ConfigParser()
    for key, values in metadata.items():
        cfg[key] = {}
        for item, value in values.items():
            cfg[key][item] = value
    try:
        with open(f"{plugin_path}/metadata.ini", 'w') as f:
            cfg.write(f)
        for plugin in global_settings.bot_plugins.values():
            if plugin.plugin_name == plugin_name:
                if plugin_name == "web_server":
                    global_settings.web_cfg = configparser.ConfigParser()
                    global_settings.web_cfg.read(f'{plugin_path}/metadata.ini')
                    plugin.metadata = global_settings.web_cfg
                else:
                    plugin.metadata = configparser.ConfigParser()
                    plugin.metadata.read(f'{plugin_path}/metadata.ini')
                if force_restart_plugin(plugin_name):
                    return True
        return False
    except IOError as e:
        log(ERROR, f"Encountered an error while updating {plugin_name} metadata file: {e}",
            origin=L_GENERAL, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False


def refresh_plugins():
    from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
    from JJMumbleBot.lib import database
    log(INFO, f"{META_NAME} is refreshing all plugins....", print_mode=PrintMode.REG_PRINT.value)
    global_settings.gui_service.quick_gui(
        f"{get_bot_name()} is refreshing all plugins.",
        text_type='header',
        box_align='left',
        ignore_whisper=True)
    for plugin in global_settings.bot_plugins.values():
        plugin.quit()
    global_settings.bot_plugins.clear()
    if global_settings.safe_mode:
        BotServiceHelper.initialize_plugins_safe()
    else:
        BotServiceHelper.initialize_plugins()
    database.init_database()
    global_settings.gui_service.quick_gui(
        f"{get_bot_name()} has refreshed all plugins.",
        text_type='header',
        box_align='left',
        ignore_whisper=True)
    log(INFO, f"{META_NAME} has refreshed all plugins.", print_mode=PrintMode.REG_PRINT.value)


def force_restart_plugin(plugin_name: str) -> bool:
    for name, plugin in global_settings.bot_plugins.items():
        if name == plugin_name:
            if name == "web_server":
                plugin.stop_server()
                return True
            else:
                plugin.stop()
                plugin.start()
                return True
    return False


def exit_bot():
    if global_settings.mumble_inst:
        global_settings.gui_service.quick_gui(
            f"{get_bot_name()} is being shutdown.",
            text_type='header',
            box_align='left',
            ignore_whisper=True,
        )
    for plugin in global_settings.bot_plugins.values():
        plugin.quit()
    if global_settings.audio_inst:
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None
        global_settings.aud_interface.exit_flag = True
        log(INFO, "Terminated audio interface instance.", origin=L_SHUTDOWN, print_mode=PrintMode.REG_PRINT.value)
    dir_utils.clear_directory(dir_utils.get_temp_med_dir())
    log(INFO, "Cleared temporary directories on shutdown.", origin=L_SHUTDOWN, print_mode=PrintMode.VERBOSE_PRINT.value)
    global_settings.exit_flag = True


def exit_bot_error(error_code: ExitCodes):
    if global_settings.mumble_inst:
        global_settings.gui_service.quick_gui(
            f"{get_bot_name()} has encountered an error and is being shutdown.<br>Please check the bot logs/console."
            f"<br>Exit Code: {error_code.value}",
            text_type='header',
            box_align='center',
            ignore_whisper=True,
        )
    try:
        for plugin in global_settings.bot_plugins.values():
            plugin.quit()
    except AttributeError:
        pass
    dir_utils.clear_directory(dir_utils.get_temp_med_dir())
    log(INFO, "Cleared temporary directories on shutdown.", origin=L_SHUTDOWN, print_mode=PrintMode.VERBOSE_PRINT.value)
    global_settings.exit_flag = True
