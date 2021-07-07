from JJMumbleBot.lib.privileges import Privileges
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.database_management_utils import save_memory_db
from JJMumbleBot.lib.utils.database_utils import CreateDB, InsertDB
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.settings import global_settings
import sqlite3
from os import path


def init_database():
    if not path.exists(f"{dir_utils.get_main_dir()}/cfg/jjmumblebot.db"):
        log(WARNING, "Bot database is missing! Generating a new database...",
            origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
        with sqlite3.connect(f"{dir_utils.get_main_dir()}/cfg/jjmumblebot.db") as conn:
            cursor = conn.cursor()
            # Create the metadata table.
            if CreateDB.create_table_metadata(db_cursor=cursor):
                log(INFO, f"Created the metadata table.",
                    origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            # Create the users table.
            if CreateDB.create_table_users(db_cursor=cursor):
                log(INFO, f"Created the users table.",
                    origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            # Create the permission levels table.
            if CreateDB.create_table_permission_levels(db_cursor=cursor):
                log(INFO, f"Created the permission levels table.",
                    origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            # Create the permissions table.
            if CreateDB.create_table_permissions(db_cursor=cursor):
                log(INFO, f"Created the user permissions table.",
                    origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            # Create the plugins table.
            if CreateDB.create_table_plugins(db_cursor=cursor):
                log(INFO, f"Created the plugins table.",
                    origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            # Create the commands table.
            if CreateDB.create_table_commands(db_cursor=cursor):
                log(INFO, f"Created the commands table.",
                    origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            # Create the aliases table.
            if CreateDB.create_table_aliases(db_cursor=cursor):
                log(INFO, f"Created the aliases table.",
                    origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            # Create the plugins_help table.
            if CreateDB.create_table_plugins_help(db_cursor=cursor):
                log(INFO, f"Created the plugins_help table.",
                    origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)

            # Create the required metadata row.
            InsertDB.insert_metadata(db_conn=conn, version=META_VERSION, checksum="N/A", ignore_file_save=True)
            log(INFO, f"Inserted default metadata information into the database.",
                origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)

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
                                    log(INFO, f"Inserted all permission level entries into the database.",
                                        origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            # Create a default super user based on the one provided in the config.ini file.
            if InsertDB.insert_new_user(db_conn=conn,
                                        username=global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU], ignore_file_save=True):
                if InsertDB.insert_new_permission(db_conn=conn,
                                                  username=global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU],
                                                  permission_level=Privileges.SUPERUSER.value, ignore_file_save=True):
                    log(INFO, f"Inserted default super user entry from config.ini file.",
                        origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            # Finished initializing the database.
            log(INFO,
                f"A new database has been created, and the default user: '{global_settings.cfg[C_CONNECTION_SETTINGS][P_DEFAULT_SU]}' has been added as a super user.",
                origin=L_DATABASE, print_mode=PrintMode.REG_PRINT.value)
            save_memory_db(mem_db_conn=conn)
            return
    with sqlite3.connect(f"{dir_utils.get_main_dir()}/cfg/jjmumblebot.db") as conn:
        save_memory_db(conn)
