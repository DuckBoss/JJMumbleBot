from JJMumbleBot.lib.utils import database_utils
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils.database_management_utils import get_memory_db


def alias_check(alias):
    alias_dict = database_utils.GetDB.get_alias(db_cursor=get_memory_db().cursor(), alias_name=alias)
    if alias_dict:
        return alias_dict['alias']
    return None


def set_alias(alias, commands) -> bool:
    if database_utils.UpdateDB.update_alias(db_conn=get_memory_db(), alias_name=alias, commands=commands):
        log(INFO, f"Registered alias: [{alias}] - [{commands}]", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    log(INFO, f"Could not register [{alias}] to the registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return False


def get_all_aliases():
    alias_list = database_utils.GetDB.get_all_aliases(db_cursor=get_memory_db().cursor())
    if alias_list is not None:
        return alias_list
    log(INFO, "Could not retrieve all the aliases from registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return []


def remove_from_aliases(alias):
    if database_utils.DeleteDB.delete_alias(db_conn=get_memory_db(), alias_name=alias):
        log(INFO, f"Removed [{alias}] from registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    log(INFO, f"Could not remove [{alias}] from registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return False


def clear_aliases():
    if database_utils.DeleteDB.delete_all_aliases(db_conn=get_memory_db()):
        log(INFO, "All aliases were removed from the registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    log(INFO, "Could not remove all aliases from registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return False


def add_to_aliases(alias, commands):
    if database_utils.InsertDB.insert_new_alias(db_conn=get_memory_db(), alias_name=alias, commands=commands):
        log(INFO, f"Registered new alias: [{alias}] - [{commands}]", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
        return True
    log(INFO, f"Could not add [{alias}] to registered aliases.", origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
    return False
