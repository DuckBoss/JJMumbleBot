from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.database_management_utils import get_memory_db, save_memory_db_to_file
from JJMumbleBot.lib.utils.database_utils import GetDB, InsertDB, UpdateDB
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.settings import global_settings as gs
from enum import Enum


class Privileges(Enum):
    BLACKLIST = 0
    DEFAULT = 1
    ELEVATED = 2
    MODERATOR = 3
    ADMINISTRATOR = 4
    SUPERUSER = 5


def privileges_check(user) -> int:
    # Print and log a critical database access error if the database has not been initialized.
    if not gs.mumble_db_string:
        log(CRITICAL,
            "The JJMumbleBot database has not been initialized, but a user privilege check is trying to access it!",
            origin=L_DATABASE, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
        return -1
    # Retrieve the user information in the database.
    user_data = GetDB.get_user_data(db_cursor=get_memory_db().cursor(), user_name=user['name'])
    # Create a new user entry if the user does not already exist in the database.
    if not user_data:
        InsertDB.insert_new_user(db_conn=get_memory_db(), username=user['name'])
        InsertDB.insert_new_permission(db_conn=get_memory_db(), username=user['name'],
                                       permission_level=Privileges.DEFAULT.value)
        # save_memory_db_to_file(get_memory_db())

        # Retrieve the user information in the database.
        user_data = GetDB.get_user_data(db_cursor=get_memory_db().cursor(), user_name=user['name'])
        return int(user_data['level'])
    return int(user_data['level'])


def plugin_privileges_check(command, plugin_name) -> int:
    if not gs.mumble_db_string:
        log(CRITICAL,
            f"The JJMumbleBot database has not been initialized, but a user privilege check is trying to access it!",
            origin=L_DATABASE, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
        return -1
    # Retrieve the command information in the database.
    command_data = GetDB.get_plugin_data(db_cursor=get_memory_db().cursor(), plugin_name=plugin_name)
    # Return the command permission level if available.
    if command_data is not None:
        for item in command_data:
            if item[0] == command:
                return int(item[1])
    # Return -1 if the command is not found.
    return -1


def plugin_privilege_checker(text, command, plugin_name) -> bool:
    if privileges_check(gs.mumble_inst.users[text.actor]) < plugin_privileges_check(command, plugin_name):
        log(WARNING,
            f"User [{gs.mumble_inst.users[text.actor]['name']}] does not have the user privileges to use this command: [{command}]",
            origin=L_USER_PRIV, error_type=GEN_PROCESS_WARN, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui(f"User [{gs.mumble_inst.users[text.actor]['name']}] does not have the user "
                                 f"privileges to use this command: [{command}]", text_type='header', box_align='left')
        return False
    return True


def get_all_privileges():
    priv_text = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>All User Privileges:</font>"
    for i, user in enumerate(GetDB.get_all_user_data(get_memory_db().cursor())):
        priv_text += f"<br><font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{user[0]}]</font> - {user[1]}"
    return priv_text


def get_blacklist():
    blklist_txt = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Blacklisted Users:</font>"
    counter = 0
    all_user_data = GetDB.get_all_user_data(get_memory_db().cursor())
    for i, user in enumerate(all_user_data):
        if int(user[1]) == int(Privileges.BLACKLIST.value):
            blklist_txt += f"<br><font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{counter}]</font> - {user[0]}"
            counter += 1
    if counter == 0:
        blklist_txt += " The blacklist is empty!"
    return blklist_txt


def add_to_blacklist(username) -> bool:
    all_user_data = GetDB.get_all_user_data(get_memory_db().cursor())
    user_names_list = [x[0] for x in all_user_data]
    if username in user_names_list:
        for user in all_user_data:
            if user[0] == username and user[1] == Privileges.BLACKLIST.value:
                log(WARNING,
                    f"Could not add the user: {username} to the blacklist since the user is already in the blacklist.",
                    origin=L_USER_PRIV, error_type=GEN_PROCESS_WARN, print_mode=PrintMode.VERBOSE_PRINT.value)
                return False
        if UpdateDB.update_user_privileges(db_conn=get_memory_db(), user_name=username, level=int(Privileges.BLACKLIST.value)):
            return True
    return False


def remove_from_blacklist(username) -> bool:
    all_user_data = GetDB.get_all_user_data(get_memory_db().cursor())
    user_names_list = [x[0] for x in all_user_data]
    if username in user_names_list:
        for user in all_user_data:
            if user[0] == username and user[1] == Privileges.BLACKLIST.value:
                if UpdateDB.update_user_privileges(db_conn=get_memory_db(), user_name=username, level=int(Privileges.DEFAULT.value)):
                    return True
    return False


def get_command_privileges(cmd_name):
    command_data = GetDB.get_command(db_cursor=get_memory_db().cursor(), command_name=cmd_name)
    return command_data


def set_command_privileges(cmd_name, level) -> bool:
    if UpdateDB.update_command_privileges(db_conn=get_memory_db(), command_name=cmd_name, permission_level=level):
        log(INFO, f"Updated command permission level: [{cmd_name}] - [{Privileges(level).name} ({level})]",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    log(INFO, f"Could not update command permission level [{cmd_name}] to the registered command.",
        origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
    return False


def import_command_permissions() -> bool:
    from JJMumbleBot.lib.utils.dir_utils import get_main_dir
    from JJMumbleBot.lib.resources.strings import T_TEMP_CMD_PERMISSIONS
    from csv import DictReader, Error
    try:
        with open(f"{get_main_dir()}/cfg/downloads/{T_TEMP_CMD_PERMISSIONS}.csv", mode='r') as csv_file:
            csvr = DictReader(csv_file)
            for i, row in enumerate(csvr):
                UpdateDB.update_command_privileges(get_memory_db(),
                                                   command_name=row['command'].strip(),
                                                   permission_level=int(row['level']),
                                                   ignore_file_save=True)
            save_memory_db_to_file()
        log(INFO, f"Updated command permissions from the imported permission file!",
            origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
        return True
    except FileNotFoundError:
        log(ERROR, f"Could not import command permissions because the downloaded file is not found!",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False
    except Error:
        log(ERROR, f"Encountered a problem reading the imported command permission file! "
                   f"Please make sure the file is correctly formatted with headers: command, level",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False
    except KeyError:
        log(ERROR, f"Encountered a problem reading the imported command permission file! "
                   f"Please make sure the file is correctly formatted with headers: command, level",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False


def import_user_privileges() -> bool:
    from JJMumbleBot.lib.utils.dir_utils import get_main_dir
    from JJMumbleBot.lib.resources.strings import T_TEMP_USER_PRIVILEGES
    from csv import DictReader, Error
    try:
        with open(f"{get_main_dir()}/cfg/downloads/{T_TEMP_USER_PRIVILEGES}.csv", mode='r') as csv_file:
            csvr = DictReader(csv_file)
            for i, row in enumerate(csvr):
                UpdateDB.update_user_privileges(get_memory_db(),
                                                user_name=row['user'].strip(),
                                                level=int(row['level']),
                                                ignore_file_save=True)
            save_memory_db_to_file()
        log(INFO, f"Updated user privileges from the imported user privileges file!",
            origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
        return True
    except FileNotFoundError:
        log(ERROR, f"Could not import user privileges because the downloaded file is not found!",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False
    except Error:
        log(ERROR, f"Encountered a problem reading the imported user privileges file! "
                   f"Please make sure the file is correctly formatted with headers: user, level",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False
    except KeyError:
        log(ERROR, f"Encountered a problem reading the imported user privileges file! "
                   f"Please make sure the file is correctly formatted with headers: user, level",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False


def set_privileges(username, level, sender) -> bool:
    all_user_data = GetDB.get_all_user_data(get_memory_db().cursor())
    user_names_list = [x[0] for x in all_user_data]
    if username in user_names_list:
        for user in all_user_data:
            if user[0] == username and username == sender:
                log(WARNING,
                    f"This user: [{username}] tried to modify their own user privileges, the modification was denied.",
                    origin=L_USER_PRIV, error_type=GEN_PROCESS_WARN, print_mode=PrintMode.VERBOSE_PRINT.value)
                return False
            if user[0] == username and privileges_check(sender) <= user[1]:
                log(WARNING,
                    f"This user: [{sender['name']}] tried to modify privileges for a user with equal/higher privileges: [{username}]",
                    origin=L_USER_PRIV, error_type=GEN_PROCESS_WARN, print_mode=PrintMode.VERBOSE_PRINT.value)
                return False
    if UpdateDB.update_user_privileges(db_conn=get_memory_db(), user_name=username, level=int(level)):
        return True
    return False


def add_to_privileges(username, level, ignore_file_save=False) -> bool:
    if InsertDB.insert_new_user(db_conn=get_memory_db(), username=username, ignore_file_save=ignore_file_save):
        if InsertDB.insert_new_permission(db_conn=get_memory_db(), username=username,
                                          permission_level=int(level), ignore_file_save=ignore_file_save):
            log(INFO,
                f"A new user: [{username}] has been added to the user privileges.",
                origin=L_USER_PRIV, print_mode=PrintMode.VERBOSE_PRINT.value)
            return True
    return False
