import os
from helpers.global_access import GlobalMods as GM


def get_config_dir():
    return os.path.join(os.path.dirname(__file__), "config.ini")


def get_main_dir():
    return os.path.dirname(__file__)


def get_bot_name():
    return GM.cfg['Connection_Settings']['UserID']


def parse_message(text):
    message = text.message.strip()
    return message


def echo(channel, message_text):
    if channel is None:
        return
    channel.send_text_message(message_text)


def get_channel(mumble, channel_name):
    return mumble.channels.find_by_name(channel_name)


def get_default_channel():
    return GM.cfg['Connection_Settings']['DefaultChannel']


def get_my_channel(mumble):
    return mumble.channels[mumble.users.myself['channel_id']]


def get_all_users(mumble):
    return mumble.users


def make_channel(mumble, root_channel, channel_name):
    return mumble.channels.new_channel(root_channel.get_id(), channel_name)


def leave(mumble):
    default_channel = get_channel(mumble, GM.cfg['Connection_Settings']['DefaultChannel'])
    default_channel.move_in()
    return default_channel


def mute(mumble):
    if GM.muted:
        return
    mumble.users.myself.mute()
    GM.muted = True
    return


def unmute(mumble):
    if not GM.muted:
        return
    mumble.users.myself.unmute()
    GM.muted = False
    return


def msg(mumble, receiver, message):
    for user in mumble.users:
        if mumble.users[user]['name'] == receiver:
            mumble.users[user].send_message(message)


def get_plugin_dir():
    return GM.cfg['Bot_Directories']['PluginsDirectory']


def get_temporary_img_dir():
    return GM.cfg['Media_Directories']['TemporaryImageDirectory']


def get_temporary_media_dir():
    return GM.cfg['Media_Directories']['TemporaryMediaDirectory']


def get_permanent_media_dir():
    return GM.cfg['Media_Directories']['PermanentMediaDirectory']


def get_vlc_dir():
    return GM.cfg['Bot_Directories']['VLCDirectory']


def get_about():
    return GM.cfg['Bot_Information']['AboutText']


def get_version():
    return GM.cfg['Bot_Information']['BotVersion']


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
