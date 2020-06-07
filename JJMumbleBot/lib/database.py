from JJMumbleBot.lib.utils.database_utils import CreateDB, InsertDB
from JJMumbleBot.lib.utils.database_management_utils import save_memory_db
from JJMumbleBot.lib.utils.print_utils import dprint, rprint
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.privileges import Privileges
import sqlite3
from os import path

user_priv_path = "cfg/jjmumblebot.db"


def init_database():
    if not path.exists(f"{dir_utils.get_main_dir()}/{user_priv_path}"):
        dprint("JJMumbleBot database is missing, creating a new database.", origin=L_DATABASE)
        log(WARNING, "JJMumbleBot database is missing, creating a new database.", origin=L_DATABASE)
        with sqlite3.connect(f"{dir_utils.get_main_dir()}/{user_priv_path}") as conn:
            cursor = conn.cursor()
            # Create the users table.
            if CreateDB.create_table_users(db_cursor=cursor):
                dprint(f"Created the users table.", origin=L_DATABASE)
                log(INFO, f"Created the users table.", origin=L_DATABASE)
            # Create the permission levels table.
            if CreateDB.create_table_permission_levels(db_cursor=cursor):
                dprint(f"Created the permission levels table.", origin=L_DATABASE)
                log(INFO, f"Created the permission levels table.", origin=L_DATABASE)
            # Create the permissions table.
            if CreateDB.create_table_permissions(db_cursor=cursor):
                dprint(f"Created the user permissions table.", origin=L_DATABASE)
                log(INFO, f"Created the user permissions table.", origin=L_DATABASE)
            # Create the plugins table.
            if CreateDB.create_table_plugins(db_cursor=cursor):
                dprint(f"Created the plugins table.", origin=L_DATABASE)
                log(INFO, f"Created the plugins table.", origin=L_DATABASE)
            # Create the commands table.
            if CreateDB.create_table_commands(db_cursor=cursor):
                dprint(f"Created the commands table.", origin=L_DATABASE)
                log(INFO, f"Created the commands table.", origin=L_DATABASE)
            # Create the aliases table.
            if CreateDB.create_table_aliases(db_cursor=cursor):
                dprint(f"Created the aliases table.", origin=L_DATABASE)
                log(INFO, f"Created the aliases table.", origin=L_DATABASE)
            # Create the plugins_help table.
            if CreateDB.create_table_plugins_help(db_cursor=cursor):
                dprint(f"Created the plugins_help table.", origin=L_DATABASE)
                log(INFO, f"Created the plugins_help table.", origin=L_DATABASE)

            # Create all the standard permission levels.
            if InsertDB.insert_new_permission_level(db_conn=conn, level_id=Privileges.BLACKLIST.value,
                                                    level_type=Privileges.BLACKLIST.name, ignore_file_save=True):
                if InsertDB.insert_new_permission_level(db_conn=conn, level_id=Privileges.DEFAULT.value,
                                                        level_type=Privileges.DEFAULT.name, ignore_file_save=True):
                    if InsertDB.insert_new_permission_level(db_conn=conn, level_id=Privileges.ELEVATED.value,
                                                            level_type=Privileges.ELEVATED.name, ignore_file_save=True):
                        if InsertDB.insert_new_permission_level(db_conn=conn, level_id=Privileges.MODERATOR.value,
                                                                level_type=Privileges.MODERATOR.name, ignore_file_save=True):
                            if InsertDB.insert_new_permission_level(db_conn=conn,
                                                                    level_id=Privileges.ADMINISTRATOR.value,
                                                                    level_type=Privileges.ADMINISTRATOR.name, ignore_file_save=True):
                                if InsertDB.insert_new_permission_level(db_conn=conn,
                                                                        level_id=Privileges.SUPERUSER.value,
                                                                        level_type=Privileges.SUPERUSER.name, ignore_file_save=True):
                                    dprint(f"Inserted all permission level entries.", origin=L_DATABASE)
                                    log(INFO, f"Inserted all permission level entries.", origin=L_DATABASE)
            # Create a default super user based on the one provided in the config.ini file.
            if InsertDB.insert_new_user(db_conn=conn,
                                        username=global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU], ignore_file_save=True):
                if InsertDB.insert_new_permission(db_conn=conn,
                                                  username=global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU],
                                                  permission_level=Privileges.SUPERUSER.value, ignore_file_save=True):
                    dprint(f"Inserted default super user entry from config.ini file.", origin=L_DATABASE)
                    log(INFO, f"Inserted default super user entry from config.ini file.", origin=L_DATABASE)
            # Finished initializing the database.
            dprint(
                f"A new database has been created, and the default user: '{global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU]}' has been added as a super user.",
                origin=L_DATABASE)
            log(INFO,
                f"A new database has been created, and the default user: '{global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU]}' has been added as a super user.",
                origin=L_DATABASE)
            save_memory_db(mem_db_conn=conn)
            return
    with sqlite3.connect(f"{dir_utils.get_main_dir()}/{user_priv_path}") as conn:
        save_memory_db(conn)
