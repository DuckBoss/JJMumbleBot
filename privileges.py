from enum import Enum
import csv
import utils
import logging
from helpers.global_access import debug_print, reg_print
from helpers.global_access import GlobalMods as GM

users = {}


class Privileges(Enum):
    BLACKLIST = 0
    DEFAULT = 1
    ELEVATED = 2
    MOD = 3
    ADMIN = 4
    OWNER = 5


def setup_privileges():
    with open(f"{utils.get_main_dir()}/privileges/privileges.csv", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        debug_print("Setting up user privileges...")
        for i, row in enumerate(csvr):
            users[row['user']] = int(row['level'])
            logging.info(f"Added [{row['user']}-{row['level']}] to the user privilege list.")


def privileges_check(user):
    if user['name'] in users.keys():
        return int(users[user['name']])

    priv_path = "privileges/privileges.csv"
    with open(f"{utils.get_main_dir()}/{priv_path}", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        for i, row in enumerate(csvr):
            if row['user'] == user['name']:
                users[user['name']] = int(row['level'])
                return int(users[user['name']])
    with open(f"{utils.get_main_dir()}/{priv_path}", mode='a', newline='') as csvf:
        headers = ['user', 'level']
        csvw = csv.DictWriter(csvf, fieldnames=headers)
        csvw.writerow({'user': user['name'], 'level': 1})
        users[user['name']] = 1
        debug_print(f"Added [{user['name']}-{user['level']}] to the user list.")
    return int(users[user['name']])


def plugin_privileges_check(command, priv_path):
    with open(f"{utils.get_plugin_dir()}/{priv_path}", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        for i, row in enumerate(csvr):
            if row['command'] == command:
                return int(row['level'])
    return -1


def plugin_privilege_checker(text, command, priv_path):
    if not privileges_check(GM.mumble.users[text.actor]) >= plugin_privileges_check(command, priv_path):
        reg_print(f"User [{GM.mumble.users[text.actor]['name']}] does not have the user privileges to use this command: [{command}]")
        GM.gui.quick_gui(f"User [{GM.mumble.users[text.actor]['name']}] does not have the user privileges to use this command: [{command}]", text_type='header', box_align='left')
        return False
    return True


def get_all_privileges():
    priv_text = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>All User Privileges:</font>"
    with open(f"{utils.get_main_dir()}/privileges/privileges.csv", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        for i, row in enumerate(csvr):
            priv_text += f"<br><font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>[{row['user']}]</font> - {row['level']}"
    return priv_text


def get_all_active_privileges():
    priv_text = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>All User Privileges:</font>"
    for i, user in enumerate(users.keys()):
        priv_text += f"<br><font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>[{row['user']}]</font> - {row['level']}"
    return priv_text


def get_blacklist():
    blklist_txt = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Blacklisted Users:</font>"
    counter = 0
    for i, user in enumerate(users.keys()):
        if users[user] == 0:
            blklist_txt += f"<br><font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>[{counter}]</font> - {user}"
            counter += 1
    if blklist_txt == f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Blacklisted Users:</font>":
        blklist_txt += "The blacklist is empty!"
    return blklist_txt


def add_to_blacklist(username, sender):
    if username in users.keys():
        if users[username] == 0:
            return False
        with open(f"{utils.get_main_dir()}/privileges/privileges.csv", mode='r') as csvf:
            csvr = csv.reader(csvf)
            content = list(csvr)
            ind = [(i, j.index(username)) for i, j in enumerate(content) if username in j]
            if int(content[ind[0][0]][1]) >= 4:
                if privileges_check(sender) == 4:
                    debug_print(f"This administrator: [{sender['name']}] tried to blacklist another administrator: [{username}]")
                    logging.warning(f"This administrator: [{sender['name']}] tried to blacklist another administrator: [{username}]")
                    return
            content[ind[0][0]][1] = 0
            users[username] = 0
            return overwrite_privileges(content)
    return False


def remove_from_blacklist(username):
    if username in users.keys():
        if users[username] == 0:
            with open(f"{utils.get_main_dir()}/privileges/privileges.csv", mode='r') as csvf:
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
            debug_print(f"This user: [{username}] tried to modify their own user privileges. Modification denied.")
            logging.warning(
                f"This user: [{username}] tried to modify their own user privileges. Modification denied.")
            return

        with open(f"{utils.get_main_dir()}/privileges/privileges.csv", mode='r') as csvf:
            csvr = csv.reader(csvf)
            content = list(csvr)
            ind = [(i, j.index(username)) for i, j in enumerate(content) if username in j]
            if int(content[ind[0][0]][1]) >= privileges_check(sender):
                if privileges_check(sender) == 4:
                    debug_print(
                        f"This administrator: [{sender['name']}] tried to modify privileges for a user with equal/higher privileges: [{username}]")
                    logging.warning(
                        f"This administrator: [{sender['name']}] tried to modify privileges for a user with equal/higher privileges: [{username}]")
                    return
            content[ind[0][0]][1] = val
            users[username] = val
            return overwrite_privileges(content)
    else:
        return False


def add_to_privileges(username, level):
    with open(f"{utils.get_main_dir()}/privileges/privileges.csv", mode='a', newline='') as csvf:
        headers = ['user', 'level']
        csvw = csv.DictWriter(csvf, fieldnames=headers)
        csvw.writerow({'user': username, 'level': level})
        users[username] = level
        debug_print(f"Added [{username}-{level}] to the user list.")
        return True


def overwrite_privileges(content):
    try:
        with open(f"{utils.get_main_dir()}/privileges/privileges.csv", mode='w', newline='') as csvf:
            csvr = csv.writer(csvf)
            csvr.writerows(content)
            return True
    except Exception:
        debug_print("There was a problem overwriting the privileges csv file.")
        logging.critical("There was a problem overwriting the privileges csv file.")
        return False
