from JJMumbleBot.settings import global_settings
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.lib.helpers import runtime_helper
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.errors import ExitCodes
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.resources.strings import *
import datetime


def parse_message(text):
    message = text.message.strip()
    user = global_settings.mumble_inst.users[text.actor]

    if message[0] == runtime_settings.cmd_token:
        rprint(f"Commands Received: [{user['name']} -> {message}]", origin=L_COMMAND)
        log(INFO, f"Commands Received: [{user['name']} -> {message}]", origin=L_COMMAND)
        # example input: !version ; !about ; !yt twice ; !p ; !status
        all_commands = [msg.strip() for msg in message.split(';')]
        # example output: ["!version", "!about", "!yt twice", "!p", "!status"]

        # add to command history
        [global_settings.cmd_history.insert(cmd) for cmd in all_commands]
        if len(all_commands) > runtime_settings.multi_cmd_limit:
            rprint(
                f"The multi-command limit was reached! The multi-command limit is {runtime_settings.multi_cmd_limit} commands per line.")
            log(WARNING,
                f"The multi-command limit was reached! The multi-command limit is {runtime_settings.multi_cmd_limit} commands per line.",
                origin=L_COMMAND)
            return
        return all_commands

    if "<img" in message:
        rprint(f"Message Received: [{user['name']} -> Image Data]")
        log(INFO, f"Message Received: [{user['name']} -> Image Data]")
    elif "<a href=" in message:
        rprint(f"Message Received: [{user['name']} -> Hyperlink Data]")
        log(INFO, f"Message Received: [{user['name']} -> Hyperlink Data]")
    else:
        rprint(f"Message Received: [{user['name']} -> {message}]")
        log(INFO, f"Message Received: [{user['name']} -> {message}]")
    return None


def mute():
    if runtime_helper.muted:
        return
    global_settings.mumble_inst.users.myself.mute()
    runtime_helper.muted = True
    return


def unmute():
    if not runtime_helper.muted:
        return
    global_settings.mumble_inst.users.myself.unmute()
    runtime_helper.muted = False
    return


def echo(channel, message_text, ignore_whisper=False):
    if channel is None:
        return
    if runtime_helper.whisper_target is not None and not ignore_whisper:
        if runtime_helper.whisper_target["type"] == 0:
            global_settings.mumble_inst.channels[runtime_helper.whisper_target["id"]].send_text_message(message_text)
        elif runtime_helper.whisper_target["type"] == 1:
            msg_id(runtime_helper.whisper_target["id"], message_text)
        elif runtime_helper.whisper_target["type"] == 2:
            for person in runtime_helper.whisper_target["id"]:
                msg_id(person, message_text)
        return
    channel.send_text_message(message_text)


def set_whisper_user(username):
    for user in global_settings.mumble_inst.users:
        if global_settings.mumble_inst.users[user]['name'] == username:
            runtime_helper.whisper_target = {"id": global_settings.mumble_inst.users[user]['session'], "type": 1}
            global_settings.mumble_inst.sound_output.set_whisper(runtime_helper.whisper_target["id"], channel=False)


def set_whisper_multi_user(users_list):
    if not isinstance(users_list, list):
        return
    whisper_targets = []
    for user in global_settings.mumble_inst.users:
        if global_settings.mumble_inst.users[user]['name'] in users_list:
            whisper_targets.append(global_settings.mumble_inst.users[user]['session'])
    if len(whisper_targets) < 1:
        return
    runtime_helper.whisper_target = {"id": whisper_targets, "type": 2}
    global_settings.mumble_inst.sound_output.set_whisper(runtime_helper.whisper_target["id"], channel=False)


def set_whisper_channel(channel_name):
    channel_id = get_channel(channel_name)['channel_id']
    runtime_helper.whisper_target = {"id": channel_id, "type": 0}
    global_settings.mumble_inst.sound_output.set_whisper(runtime_helper.whisper_target["id"], channel=True)


def get_whisper_clients_by_type(wh_type: int):
    if runtime_helper.whisper_target is None:
        return None
    if wh_type == 0:
        return global_settings.mumble_inst.channels[runtime_helper.whisper_target['id']]['name']
    if wh_type == 1:
        for user in global_settings.mumble_inst.users:
            if global_settings.mumble_inst.users[user]['session'] == runtime_helper.whisper_target['id']:
                return global_settings.mumble_inst.users[user]['name']
    else:
        user_list = []
        for user in global_settings.mumble_inst.users:
            if global_settings.mumble_inst.users[user]['session'] == runtime_helper.whisper_target['id']:
                user_list.append(global_settings.mumble_inst.users[user]['name'])
        return user_list


def clear_whisper():
    runtime_helper.whisper_target = None
    global_settings.mumble_inst.sound_output.remove_whisper()


def msg(receiver, message):
    for user in global_settings.mumble_inst.users:
        if global_settings.mumble_inst.users[user]['name'] == receiver:
            global_settings.mumble_inst.users[user].send_text_message(message)


def msg_id(receiver_id, message):
    for user in global_settings.mumble_inst.users:
        if global_settings.mumble_inst.users[user]['session'] == receiver_id:
            global_settings.mumble_inst.users[user].send_text_message(message)


def get_command_token():
    return runtime_settings.cmd_token


def get_bot_name():
    return global_settings.cfg[C_CONNECTION_SETTINGS][P_USER_ID]


def get_bot_internal_name():
    return META_NAME


def get_channel(channel_name):
    return global_settings.mumble_inst.channels.find_by_name(channel_name)


def get_default_channel():
    return global_settings.cfg[C_CONNECTION_SETTINGS][P_CHANNEL_DEF]


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
    users = cur_channel.get_users()
    return users


def make_channel(root_channel, channel_name):
    from json import loads
    allowed_channels = loads(global_settings.cfg[C_PLUGIN_SETTINGS][P_PLUG_ALLOWED_CHANNELS])
    if allowed_channels is not None:
        for chan_name in allowed_channels:
            found_channel = global_settings.mumble_inst.channels.find_by_name(chan_name)
            if found_channel is not None and found_channel.get_id() == root_channel.get_id():
                return global_settings.mumble_inst.channels.new_channel(root_channel.get_id(), channel_name)
    return None


def leave_channel():
    default_channel = get_channel(global_settings.cfg[C_CONNECTION_SETTINGS][P_CHANNEL_DEF])
    default_channel.move_in()


def remove_channel():
    cur_channel = get_my_channel()
    cur_channel.remove()


def check_up_time():
    cur_time = datetime.datetime.now() - runtime_helper.start_time
    return f"{str(cur_time)[:-7]}"


def refresh_plugins():
    from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
    from JJMumbleBot.lib import database
    dprint("Refreshing all plugins...")
    log(INFO, f"{META_NAME} is refreshing all plugins....")
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
    dprint("All plugins refreshed.")
    global_settings.gui_service.quick_gui(
        f"{get_bot_name()} has refreshed all plugins.",
        text_type='header',
        box_align='left',
        ignore_whisper=True)
    log(INFO, f"{META_NAME} has refreshed all plugins.")


def exit_bot():
    from JJMumbleBot.lib.utils import dir_utils
    global_settings.gui_service.quick_gui(
        f"{get_bot_name()} is being shutdown.",
        text_type='header',
        box_align='left',
        ignore_whisper=True,
    )
    for plugin in global_settings.bot_plugins.values():
        plugin.quit()
    if global_settings.flask_server:
        global_settings.flask_server.stop()
        dprint("Terminated flask server instance.", origin=L_WEB_INTERFACE)
    if global_settings.socket_server:
        global_settings.socket_server = None
        dprint("Terminated web socket server instance.", origin=L_WEB_INTERFACE)
    dir_utils.clear_directory(dir_utils.get_temp_med_dir())
    dprint("Cleared temporary directories on shutdown.")
    log(INFO, "Cleared temporary directories on shutdown.", origin=L_SHUTDOWN)
    global_settings.exit_flag = True


def exit_bot_error(error_code: ExitCodes):
    from JJMumbleBot.lib.utils import dir_utils
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
    dprint("Cleared temporary directories on shutdown.")
    log(INFO, "Cleared temporary directories on shutdown.", origin=L_SHUTDOWN)
    global_settings.exit_flag = True
