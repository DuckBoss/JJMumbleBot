from enum import Enum
import csv
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.print_utils import dprint, rprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.helpers.bot_service_helper import BotServiceHelper
from JJMumbleBot.lib.resources.strings import *

users = {}


class Privileges(Enum):
    BLACKLIST = 0
    DEFAULT = 1
    ELEVATED = 2
    MOD = 3
    ADMIN = 4
    OWNER = 5


user_priv_path = "cfg/user_privileges.csv"


def setup_privileges():
    with open(f"{dir_utils.get_main_dir()}/{user_priv_path}", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        dprint("Setting up user privileges...")
        for i, row in enumerate(csvr):
            users[row['user']] = int(row['level'])
            BotServiceHelper.log(INFO, f"Added [{row['user']}-{row['level']}] to the user privileges list.")


def privileges_check(user):
    if user['name'] in users.keys():
        return int(users[user['name']])
    with open(f"{dir_utils.get_main_dir()}/{user_priv_path}", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        for i, row in enumerate(csvr):
            if row['user'] == user['name']:
                users[user['name']] = int(row['level'])
                return int(users[user['name']])
    with open(f"{dir_utils.get_main_dir()}/{user_priv_path}", mode='a', newline='') as csvf:
        headers = ['user', 'level']
        csvw = csv.DictWriter(csvf, fieldnames=headers)
        csvw.writerow({'user': user['name'], 'level': 1})
        users[user['name']] = 1
        dprint(f"Added [{user['name']}-{users[user['name']]}] to the user privileges list.")
    return int(users[user['name']])


def plugin_privileges_check(command, priv_path):
    with open(f"{dir_utils.get_main_dir()}/{priv_path}", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        for i, row in enumerate(csvr):
            if row['command'] == command:
                return int(row['level'])
    return -1


def plugin_privilege_checker(text, command, priv_path):
    if not privileges_check(GS.mumble_inst.users[text.actor]) >= plugin_privileges_check(command, priv_path):
        rprint(
            f"User [{GS.mumble_inst.users[text.actor]['name']}] does not have the user privileges to use this command: [{command}]")
        GS.gui_service.quick_gui(f"User [{GS.mumble_inst.users[text.actor]['name']}] does not have the user "
                                 f"privileges to use this command: [{command}]", text_type='header', box_align='left')
        return False
    return True


def get_all_privileges():
    priv_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>All User Privileges:</font>"
    with open(f"{dir_utils.get_main_dir()}/{user_priv_path}", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        for i, row in enumerate(csvr):
            priv_text += f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{row['user']}]</font> - {row['level']}"
    return priv_text


def get_blacklist():
    blklist_txt = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Blacklisted Users:</font>"
    counter = 0
    for i, user in enumerate(users.keys()):
        if users[user] == 0:
            blklist_txt += f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{counter}]</font> - {user}"
            counter += 1
    if blklist_txt == f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Blacklisted Users:</font>":
        blklist_txt += "The blacklist is empty!"
    return blklist_txt


def add_to_blacklist(username, sender):
    if username in users.keys():
        if users[username] == 0:
            return False
        with open(f"{dir_utils.get_main_dir()}/{user_priv_path}", mode='r') as csvf:
            csvr = csv.reader(csvf)
            content = list(csvr)
            ind = [(i, j.index(username)) for i, j in enumerate(content) if username in j]
            if int(content[ind[0][0]][1]) >= 4:
                if privileges_check(sender) == 4:
                    dprint(
                        f"This administrator: [{sender['name']}] tried to blacklist another administrator: [{username}]")
                    BotServiceHelper.log(WARNING,
                                         f"This administrator: [{sender['name']}] tried to blacklist another administrator: [{username}]")
                    return
            content[ind[0][0]][1] = 0
            users[username] = 0
            return overwrite_privileges(content)
    return False


def remove_from_blacklist(username):
    if username in users.keys():
        if users[username] == 0:
            with open(f"{dir_utils.get_main_dir()}/{user_priv_path}", mode='r') as csvf:
                csvr = csv.reader(csvf)
                content = list(csvr)
                ind = [(i, j.index(username)) for i, j in enumerate(content) if username in j]
                content[ind[0][0]][1] = 1
                users[username] = 1
                return overwrite_privileges(content)
        else:
            return False
    return False


def set_privileges(username, val, sender):
    if username in users.keys():
        if username == sender['name']:
            dprint(f"This user: [{username}] tried to modify their own user privileges. Modification denied.")
            BotServiceHelper.log(WARNING,
                                 f"This user: [{username}] tried to modify their own user privileges. Modification denied.")
            return

        with open(f"{dir_utils.get_main_dir()}/{user_priv_path}", mode='r') as csvf:
            csvr = csv.reader(csvf)
            content = list(csvr)
            ind = [(i, j.index(username)) for i, j in enumerate(content) if username in j]
            if int(content[ind[0][0]][1]) >= privileges_check(sender):
                if privileges_check(sender) == 4:
                    dprint(
                        f"This administrator: [{sender['name']}] tried to modify privileges for a user with equal/higher privileges: [{username}]")
                    BotServiceHelper.log(WARNING,
                                         f"This administrator: [{sender['name']}] tried to modify privileges for a user with equal/higher privileges: [{username}]")
                    return
            content[ind[0][0]][1] = val
            users[username] = val
            return overwrite_privileges(content)
    else:
        return False


def add_to_privileges(username, level):
    with open(f"{dir_utils.get_main_dir()}/{user_priv_path}", mode='a', newline='') as csvf:
        headers = ['user', 'level']
        csvw = csv.DictWriter(csvf, fieldnames=headers)
        csvw.writerow({'user': username, 'level': level})
        users[username] = level
        dprint(f"Added [{username}-{level}] to the user list.")
        return True


# TODO: Modify generic exception to a specific one.
def overwrite_privileges(content):
    try:
        with open(f"{dir_utils.get_main_dir()}/{user_priv_path}", mode='w', newline='') as csvf:
            csvr = csv.writer(csvf)
            csvr.writerows(content)
            return True
    except Exception:
        dprint("There was a problem overwriting the privileges csv file.")
        BotServiceHelper.log(WARNING, "There was a problem overwriting the privileges csv file.")
        return False
