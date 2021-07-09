from JJMumbleBot.lib.utils.database_utils import GetDB, DeleteDB, UpdateDB, InsertDB
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils.database_management_utils import get_memory_db, save_memory_db_to_file


def alias_check(alias):
    alias_dict = GetDB.get_alias(db_cursor=get_memory_db().cursor(), alias_name=alias)
    if alias_dict:
        return alias_dict['alias']
    return None


def set_alias(alias, commands) -> bool:
    if UpdateDB.update_alias(db_conn=get_memory_db(), alias_name=alias, commands=commands):
        log(INFO, f"Registered alias: [{alias}] - [{commands}]", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    log(INFO, f"Could not register [{alias}] to the registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return False


def get_all_aliases():
    alias_list = GetDB.get_all_aliases(db_cursor=get_memory_db().cursor())
    if alias_list is not None:
        return alias_list
    log(INFO, "Could not retrieve all the aliases from registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return []


def remove_from_aliases(alias):
    if DeleteDB.delete_alias(db_conn=get_memory_db(), alias_name=alias):
        log(INFO, f"Removed [{alias}] from registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    log(INFO, f"Could not remove [{alias}] from registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return False


def clear_aliases():
    if DeleteDB.delete_all_aliases(db_conn=get_memory_db()):
        log(INFO, "All aliases were removed from the registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    log(INFO, "Could not remove all aliases from registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return False


def add_to_aliases(alias, commands):
    if InsertDB.insert_new_alias(db_conn=get_memory_db(), alias_name=alias, commands=commands):
        log(INFO, f"Registered new alias: [{alias}] - [{commands}]", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    log(INFO, f"Could not add [{alias}] to registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return False


def import_aliases() -> bool:
    from JJMumbleBot.lib.utils.dir_utils import get_main_dir
    from JJMumbleBot.lib.resources.strings import T_TEMP_ALIASES
    from csv import DictReader, Error
    try:
        with open(f"{get_main_dir()}/cfg/downloads/{T_TEMP_ALIASES}.csv", mode='r') as csv_file:
            csvr = DictReader(csv_file)
            for i, row in enumerate(csvr):
                UpdateDB.update_alias(get_memory_db(),
                                      alias_name=row['alias'].strip(),
                                      commands=row['command'].strip(),
                                      ignore_file_save=True)
            save_memory_db_to_file()
        log(INFO, f"Updated aliases from the imported aliases file!",
            origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
        return True
    except FileNotFoundError:
        log(ERROR, f"Could not import aliases because the downloaded file is not found!",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False
    except Error:
        log(ERROR, f"Encountered a problem reading the imported aliases file! "
                   f"Please make sure the file is correctly formatted with headers: alias, command",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False
    except KeyError:
        log(ERROR, f"Encountered a problem reading the imported aliases file! "
                   f"Please make sure the file is correctly formatted with headers: alias, command",
            origin=L_DATABASE, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False
