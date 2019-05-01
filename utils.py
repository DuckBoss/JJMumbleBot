import os
from helpers.global_access import GlobalMods as GM


def get_config_dir():
    return os.path.join(os.path.dirname(__file__), "config.ini")


def get_main_dir():
    return os.path.dirname(__file__)


def get_bot_name():
    return GM.cfg['Connection_Settings']['UserID']


def get_tests_dir():
    return os.path.join(os.path.dirname(__file__), "/tests")


def get_templates_dir():
    return os.path.join(os.path.dirname(__file__), "/templates")


def set_whisper_user(username):
    for user in GM.mumble.users:
        if GM.mumble.users[user]['name'] == username:
            GM.whisper_target = {"id": GM.mumble.users[user]['session'], "type": 1}
            GM.mumble.sound_output.set_whisper(GM.whisper_target["id"], channel=False)


def set_whisper_multi_user(users_list):
    if not isinstance(users_list, list):
        return
    GM.whisper_target = {"id": users_list, "type": 2}
    GM.mumble.sound_output.set_whisper(GM.whisper_target["id"], channel=False)


def set_whisper_channel(channel_name):
    channel_id = get_channel(channel_name)['channel_id']
    GM.whisper_target = {"id": channel_id, "type": 0}
    GM.mumble.sound_output.set_whisper(GM.whisper_target["id"], channel=True)


def clear_whisper():
    GM.whisper_target = None
    GM.mumble.sound_output.remove_whisper()


def parse_message(text):
    message = text.message.strip()
    return message


def echo(channel, message_text, ignore_whisper=False):
    if channel is None:
        return
    if GM.whisper_target is not None and not ignore_whisper:
        if GM.whisper_target["type"] == 0:
            GM.mumble.channels[GM.whisper_target["id"]].send_text_message(message_text)
        elif GM.whisper_target["type"] == 1:
            msg_id(GM.whisper_target["id"], message_text)
        elif GM.whisper_target["type"] == 2:
            for person in GM.whisper_target["id"]:
                msg_id(person, message_text)
        return
    channel.send_text_message(message_text)


def echo_my_channel(message_text):
    get_my_channel().send_text_message(message_text)


def get_channel(channel_name):
    return GM.mumble.channels.find_by_name(channel_name)


def get_default_channel():
    return GM.cfg['Connection_Settings']['DefaultChannel']


def get_my_channel():
    return GM.mumble.channels[GM.mumble.users.myself['channel_id']]


def get_all_users():
    return GM.mumble.users


def make_channel(root_channel, channel_name):
    return GM.mumble.channels.new_channel(root_channel.get_id(), channel_name)


def leave():
    default_channel = get_channel(GM.cfg['Connection_Settings']['DefaultChannel'])
    default_channel.move_in()
    return default_channel


def mute():
    if GM.muted:
        return
    GM.mumble.users.myself.mute()
    GM.muted = True
    return


def unmute():
    if not GM.muted:
        return
    GM.mumble.users.myself.unmute()
    GM.muted = False
    return


def msg(receiver, message):
    for user in GM.mumble.users:
        if GM.mumble.users[user]['name'] == receiver:
            GM.mumble.users[user].send_text_message(message)


def msg_id(receiver_id, message):
    for user in GM.mumble.users:
        if GM.mumble.users[user]['session'] == receiver_id:
            GM.mumble.users[user].send_text_message(message)


def get_plugin_dir():
    return GM.cfg['Bot_Directories']['PluginsDirectory']


def get_temporary_img_dir():
    return GM.cfg['Media_Directories']['TemporaryImageDirectory']


def get_permanent_media_dir():
    return GM.cfg['Media_Directories']['PermanentMediaDirectory']


def get_vlc_dir():
    return GM.cfg['Bot_Directories']['VLCDirectory']


def get_about():
    return GM.cfg['Bot_Information']['AboutText']


def get_version():
    return GM.version


def get_known_bugs():
    return GM.cfg['Bot_Information']['KnownBugs']


def clear_directory(d):
    for the_file in os.listdir(d):
        file_path = os.path.join(d, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def remove_file(f, d):
    for the_file in os.listdir(d):
        try:
            file_path = os.path.join(d, the_file)
            if os.path.isfile(file_path):
                if the_file == f:
                    os.unlink(file_path)
        except Exception as e:
            print(e)


def make_directory(d):
    if not os.path.exists(d):
        os.makedirs(d)
