import privileges as pv
import os
from helpers.config_access import GlobalMods as CFG


def get_config_dir():
    return os.path.join(os.path.dirname(__file__), "config.ini")


def get_main_dir():
    return os.path.dirname(__file__)


def get_bot_name():
    return CFG.cfg_inst['Connection_Settings']['UserID']


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
    return CFG.cfg_inst['Connection_Settings']['DefaultChannel']


def get_my_channel(mumble):
    return mumble.channels[mumble.users.myself['channel_id']]


def get_all_users(mumble):
    return mumble.users


def make_channel(mumble, root_channel, channel_name):
    return mumble.channels.new_channel(root_channel.get_id(), channel_name)


def leave(mumble):
    default_channel = get_channel(mumble, CFG.cfg_inst['Connection_Settings']['DefaultChannel'])
    default_channel.move_in()
    return default_channel


def mute(mumble):
    mumble.users.myself.mute()


def unmute(mumble):
    mumble.users.myself.unmute()


def msg(mumble, receiver, message):
    for user in mumble.users:
        if mumble.users[user]['name'] == receiver:
            mumble.users[user].send_message(message)


def setup_privileges():
    with open("%s/privileges/blacklist.txt" % get_main_dir()) as blklist:
        line = blklist.readline()
        pv.blacklist_names.append(line.strip())
    with open("%s/privileges/admin.txt" % get_main_dir()) as admlist:
        line = admlist.readline()
        pv.admin_names.append(line.strip())
    print("User privilege setup complete.")


def privileges_check(user):
    blacklist_names = pv.blacklist_names
    admin_names = pv.admin_names
    if user['name'] in blacklist_names:
        print("User %s tried to enter a command. Request denied." % user['name'])
        return pv.Privileges.BLACKLIST
    elif user['name'] in admin_names:
        # print("User %s is an admin." % user['name'])
        return pv.Privileges.ADMIN
    return pv.Privileges.NORMAL


def get_blacklist():
    blklist_txt = "<br><font color='red'>Blacklist:</font><br>"
    try:
        with open("%s/privileges/blacklist.txt" % get_main_dir(), 'r') as blklist:
            lines = blklist.readlines()
        for i, item in enumerate(lines):
            blklist_txt += "<font color='cyan'>[%d]: </font><font color='yellow'>%s</font><br>" % (i, item.strip())
        return blklist_txt
    except Exception:
        print("File could not be opened.")
    return blklist_txt


def add_to_blacklist(user_name):
    try:
        if user_name not in pv.blacklist_names:
            with open("%s/privileges/blacklist.txt" % get_main_dir(), 'a') as blklist:
                blklist.write("%s\n" % user_name)
                pv.blacklist_names.append(user_name)
                print("User %s added to the blacklist." % user_name)
                return True
    except Exception as e:
        print("Unable to add %s to the blacklist. {%s}" % (user_name, e))
        return False
    print("%s is already in the blacklist." % user_name)
    return False


def remove_from_blacklist(user_name):
    try:
        if user_name in pv.blacklist_names:
            with open("%s/privileges/blacklist.txt" % get_main_dir(), 'r') as blklist:
                lines = blklist.readlines()
            with open("%s/privileges/blacklist.txt" % get_main_dir(), 'w') as blklist:
                for line in lines:
                    if line != ("%s\n" % user_name):
                        blklist.write(line)
                pv.blacklist_names.remove(user_name)
                print("User %s removed from the blacklist." % user_name)
                return True
    except Exception as e:
        print("Unable to remove %s from the blacklist. {%s}" % (user_name, e))
        return False
    print("%s is not in the blacklist." % user_name)
    return False


def get_plugin_dir():
    return CFG.cfg_inst['Bot_Directories']['PluginsDirectory']

def get_temporary_img_dir():
    return CFG.cfg_inst['Media_Directories']['TemporaryImageDirectory']


def get_temporary_media_dir():
    return CFG.cfg_inst['Media_Directories']['TemporaryMediaDirectory']


def get_permanent_media_dir():
    return CFG.cfg_inst['Media_Directories']['PermanentMediaDirectory']


def get_vlc_dir():
    return CFG.cfg_inst['Bot_Directories']['VLCDirectory']


def get_about():
    return CFG.cfg_inst['Bot_Information']['AboutText']


def get_version():
    return CFG.cfg_inst['Bot_Information']['BotVersion']


def get_known_bugs():
    return CFG.cfg_inst['Bot_Information']['KnownBugs']


def clear_directory(d):
    for the_file in os.listdir(d):
        file_path = os.path.join(d, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def make_directory(d):
    if not os.path.exists(d):
        os.makedirs(d)
