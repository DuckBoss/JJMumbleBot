from csv import DictReader
from sqlite3 import Error
from JJMumbleBot.lib.utils.print_utils import dprint
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.database_management_utils import save_memory_db, save_memory_db_to_file
from JJMumbleBot.lib.resources.strings import *


class CreateDB:
    @staticmethod
    def create_table_users(db_cursor) -> bool:
        table_query = """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """
        try:
            db_cursor.execute(table_query)
            return True
        except Error as err:
            dprint(err)
            log(WARNING, f'There was an error creating the users table in the user_privileges database: {err}')
            return False

    @staticmethod
    def create_table_permissions(db_cursor) -> bool:
        table_query = """
            CREATE TABLE IF NOT EXISTS permissions (
                user_id INTEGER UNIQUE PRIMARY KEY,
                level INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (level) REFERENCES permission_levels(level_id)
            );
        """
        try:
            db_cursor.execute(table_query)
            return True
        except Error as err:
            dprint(err)
            log(WARNING, f'There was an error creating the permissions table in the user_privileges database: {err}')
            return False

    @staticmethod
    def create_table_permission_levels(db_cursor) -> bool:
        table_query = """
            CREATE TABLE IF NOT EXISTS permission_levels (
                level_id INTEGER UNIQUE PRIMARY KEY,
                level_type TEXT NOT NULL
            );
        """
        try:
            db_cursor.execute(table_query)
            return True
        except Error as err:
            dprint(err)
            log(WARNING, f'There was an error creating the users table in the user_privileges database: {err}')
            return False

    @staticmethod
    def create_table_plugins(db_cursor) -> bool:
        table_query = """
            CREATE TABLE IF NOT EXISTS plugins (
                plugin_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        """
        try:
            db_cursor.execute(table_query)
            return True
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def create_table_commands(db_cursor) -> bool:
        table_query = """
            CREATE TABLE IF NOT EXISTS commands (
                command_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                plugin_id INTEGER NOT NULL,
                name TEXT UNIQUE NOT NULL,
                level INTEGER NOT NULL,
                FOREIGN KEY (plugin_id) REFERENCES plugins(plugin_id),
                FOREIGN KEY (level) REFERENCES permission_levels(level_id)
            );
        """
        try:
            db_cursor.execute(table_query)
            return True
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def create_table_aliases(db_cursor) -> bool:
        table_query = """
            CREATE TABLE IF NOT EXISTS aliases (
                alias_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                alias TEXT NOT NULL
            );
        """
        try:
            db_cursor.execute(table_query)
            return True
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def create_table_plugins_help(db_cursor) -> bool:
        table_query = """
            CREATE TABLE IF NOT EXISTS plugins_help (
                help_id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                plugin_id INTEGER UNIQUE NOT NULL,
                help_text TEXT NOT NULL,
                FOREIGN KEY (plugin_id) REFERENCES plugins(plugin_id)
            );
        """
        try:
            db_cursor.execute(table_query)
            return True
        except Error as err:
            dprint(err)
            return False


class InsertDB:
    @staticmethod
    def insert_new_plugin(db_conn, plugin_name, ignore_file_save=False) -> bool:
        table_query = f"""
            INSERT INTO plugins(name)
            VALUES (
            ?
            );
        """
        try:
            db_conn.cursor().execute(table_query, (plugin_name, ))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Inserted new plugin into the database: {plugin_name}",
                       origin=L_DATABASE)
                log(INFO, f"Inserted new plugin into the database: {plugin_name}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            if 'UNIQUE' not in str(err):
                dprint(err)
            return False

    @staticmethod
    def insert_new_command(db_conn, plugin_name, command_name, permission_level, ignore_file_save=False) -> bool:
        table_query = f"""
            INSERT INTO commands(plugin_id, name, level)
            VALUES (
            (SELECT plugins.plugin_id FROM plugins WHERE plugins.name = ? LIMIT 1),
            ?,
            ?
            );
        """
        try:
            db_conn.cursor().execute(table_query, (plugin_name, command_name, permission_level))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Inserted new command into the database: {plugin_name}-{command_name}-{permission_level}", origin=L_DATABASE)
                log(INFO, f"Inserted new command into the database: {plugin_name}-{command_name}-{permission_level}", origin=L_DATABASE)
                return True
            return False
        except Error as err:
            if 'UNIQUE' not in str(err):
                dprint(err)
            return False

    @staticmethod
    def insert_new_plugins_help(db_conn, plugin_name, help_text, ignore_file_save=False) -> bool:
        table_query = f"""
            INSERT INTO plugins_help(plugin_id, help_text)
            VALUES (
            (SELECT plugins.plugin_id FROM plugins WHERE plugins.name = ? LIMIT 1),
            ?
            );
        """
        try:
            db_conn.cursor().execute(table_query, (plugin_name, help_text))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Inserted new plugin help data into the database: {plugin_name}",
                       origin=L_DATABASE)
                log(INFO, f"Inserted new plugin help data into the database: {plugin_name}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            if 'UNIQUE' not in str(err):
                dprint(err)
            return False

    @staticmethod
    def insert_new_alias(db_conn, alias_name, commands, ignore_file_save=False) -> bool:
        table_query = f"""
                INSERT INTO aliases(name, alias)
                VALUES (
                ?,
                ?
                );
            """
        try:
            db_conn.cursor().execute(table_query, (alias_name, commands))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Inserted new alias into the database: {alias_name}",
                       origin=L_DATABASE)
                log(INFO, f"Inserted new alias into the database: {alias_name}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            if 'UNIQUE' not in str(err):
                dprint(err)
            return False

    @staticmethod
    def insert_new_user(db_conn, username: str, ignore_file_save=False) -> bool:
        table_query = f"""
            INSERT INTO users (name)
            VALUES (?);
        """
        try:
            db_conn.cursor().execute(table_query, (username, ))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Inserted new user into the database: {username}",
                       origin=L_DATABASE)
                log(INFO, f"Inserted new user into the database: {username}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def insert_new_permission_level(db_conn, level_id: int, level_type: str, ignore_file_save=False) -> bool:
        table_query = f"""
            INSERT INTO permission_levels(level_id, level_type)
            VALUES (
            ?, 
            ?
            );
        """
        try:
            db_conn.cursor().execute(table_query, (level_id, level_type))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Inserted new permission level into the database: {level_id}-{level_type}",
                       origin=L_DATABASE)
                log(INFO, f"Inserted new permission level into the database: {level_id}-{level_type}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def insert_new_permission(db_conn, username: str, permission_level: int, ignore_file_save=False) -> bool:
        table_query = f"""
            INSERT INTO permissions(user_id, level)
            VALUES (
            (SELECT users.user_id FROM users WHERE users.name = ? LIMIT 1), 
            (SELECT permission_levels.level_id FROM permission_levels WHERE permission_levels.level_id = ? LIMIT 1)
            );
        """
        try:
            db_conn.cursor().execute(table_query, (username, permission_level))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Inserted new permission into the database: {username}-{permission_level}",
                       origin=L_DATABASE)
                log(INFO, f"Inserted new permission into the database: {username}-{permission_level}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False


class DeleteDB:
    @staticmethod
    def delete_user(db_conn, user_id: int = None, user_name: str = None, ignore_file_save=False) -> bool:
        if user_id is None and user_name is None:
            return False
        delete_permission_query = ""
        delete_user_query = ""
        if user_id:
            delete_permission_query = f"""
                DELETE FROM permissions
                WHERE permissions.user_id = ?
            """
            delete_user_query = f"""
                DELETE FROM users
                WHERE users.user_id = ?
            """
        elif user_name:
            delete_permission_query = f"""
                DELETE FROM permissions
                WHERE permissions.user_id = (SELECT users.user_id FROM users WHERE users.name = ? LIMIT 1);
            """
            delete_user_query = f"""
                DELETE FROM users
                WHERE users.name = ?;
            """
        try:
            db_conn.cursor().execute(delete_permission_query, (user_id if user_id is not None else user_name, ))
            db_conn.cursor().execute(delete_user_query, (user_id if user_id is not None else user_name, ))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount > 0:
                dprint(f"Deleted alias in the database: {user_id if user_id is not None else user_name}",
                       origin=L_DATABASE)
                log(INFO, f"Deleted alias in the database: {user_id if user_id is not None else user_name}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def delete_alias(db_conn, alias_id: int = None, alias_name: str = None, ignore_file_save=False) -> bool:
        if alias_id is None and alias_name is None:
            return False
        delete_alias_query = ""
        if alias_id:
            delete_alias_query = f"""
                    DELETE FROM aliases
                    WHERE aliases.alias_id = ?
                """
        elif alias_name:
            delete_alias_query = f"""
                    DELETE FROM aliases
                    WHERE aliases.name = ?;
                """
        try:
            db_conn.cursor().execute(delete_alias_query, (alias_id if alias_id is not None else alias_name, ))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if alias_id is not None:
                if GetDB.get_alias(db_cursor=db_conn.cursor(), alias_id=alias_id) is None:
                    dprint(f"Deleted alias in the database: {alias_id}",
                           origin=L_DATABASE)
                    log(INFO, f"Deleted alias in the database: {alias_id}",
                        origin=L_DATABASE)
                    return True
            else:
                if GetDB.get_alias(db_cursor=db_conn.cursor(), alias_name=alias_name) is None:
                    dprint(f"Deleted alias in the database: {alias_name}",
                           origin=L_DATABASE)
                    log(INFO, f"Deleted alias in the database: {alias_name}",
                        origin=L_DATABASE)
                    return True
            return False
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def delete_all_aliases(db_conn, ignore_file_save=False):
        # Output Format: [(name, alias), (name, alias), ...]
        delete_aliases_query = f"""
            DELETE FROM aliases;
        """
        try:
            db_conn.cursor().execute(delete_aliases_query)
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount > 0:
                dprint(f"Deleted all alias in the database",
                       origin=L_DATABASE)
                log(INFO, f"Deleted all alias in the database",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def delete_all_plugins(db_conn, ignore_file_save=False):
        delete_plugins_query = f"""
                DELETE FROM plugins;
            """
        try:
            db_conn.cursor().execute(delete_plugins_query)
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount > 0:
                dprint(f"Deleted all plugins in the database",
                       origin=L_DATABASE)
                log(INFO, f"Deleted all plugins in the database",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def delete_all_plugins_help(db_conn, ignore_file_save=False):
        delete_plugins_help_query = f"""
                    DELETE FROM plugins_help;
                """
        try:
            db_conn.cursor().execute(delete_plugins_help_query)
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount > 0:
                dprint(f"Deleted all plugins_help in the database",
                       origin=L_DATABASE)
                log(INFO, f"Deleted all plugins_help in the database",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def delete_all_commands(db_conn, ignore_file_save=False):
        delete_commands_query = f"""
                        DELETE FROM commands;
                    """
        try:
            db_conn.cursor().execute(delete_commands_query)
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount > 0:
                dprint(f"Deleted all commands in the database",
                       origin=L_DATABASE)
                log(INFO, f"Deleted all commands in the database",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False


class GetDB:
    @staticmethod
    def get_user_data(db_cursor, user_id: int = None, user_name: str = None):
        # Output Dict: {user_id: str, name: str, level: int, level_type: str}
        if user_id is None and user_name is None:
            return None
        get_user_query = ""
        if user_id:
            get_user_query = f"""
                SELECT users.user_id, users.name, permissions.level, permission_levels.level_type
                FROM users, permissions, permission_levels
                WHERE users.user_id = ?
                AND users.user_id = permissions.user_id
                AND permissions.level = permission_levels.level_id
                LIMIT 1;
            """
        elif user_name:
            get_user_query = f"""
                SELECT users.user_id, users.name, permissions.level, permission_levels.level_type
                FROM users, permissions, permission_levels
                WHERE users.name = ?
                AND users.user_id = permissions.user_id
                AND permissions.level = permission_levels.level_id;
            """
        try:
            db_cursor.execute(get_user_query, (user_id if user_id is not None else user_name, ))
            result_dict = {}
            result_cols = [item[0] for item in db_cursor.description]
            result_row = db_cursor.fetchone()
            if result_row is None:
                return None
            for i, item in enumerate(result_cols):
                result_dict[item] = list(result_row)[i]
            return result_dict
        except Error as err:
            dprint(err)
            return None

    @staticmethod
    def get_all_user_data(db_cursor):
        # Output Format: [(user, level), (user, level), ...]
        get_plugin_query = f"""SELECT users.user_id, users.name FROM users"""
        try:
            db_cursor.execute(get_plugin_query)
            result_list = []
            result_row = db_cursor.fetchall()
            if result_row is None:
                return None
            for i, item in enumerate(result_row):
                user_data = GetDB.get_user_data(db_cursor=db_cursor, user_id=list(result_row)[i][0])
                result_list.append((user_data['name'], user_data['level']))
            return result_list
        except Error as err:
            dprint(err)
            return None

    @staticmethod
    def get_alias(db_cursor, alias_id: int = None, alias_name: str = None):
        # Output Dict: {alias_id: int, alias_name: str, commands: List[str]}
        if alias_id is None and alias_name is None:
            return None
        get_user_query = ""
        if alias_id:
            get_user_query = f"""
                        SELECT alias_id, name, alias
                        FROM aliases
                        WHERE aliases.alias_id = ?
                        LIMIT 1;
                    """
        elif alias_name:
            get_user_query = f"""
                        SELECT alias_id, name, alias
                        FROM aliases
                        WHERE aliases.name = ?
                        LIMIT 1;
                    """
        try:
            db_cursor.execute(get_user_query, (alias_id if alias_id is not None else alias_name, ))
            result_dict = {}
            result_cols = [item[0] for item in db_cursor.description]
            result_row = db_cursor.fetchone()
            if result_row is None:
                return None
            for i, item in enumerate(result_cols):
                result_dict[item] = list(result_row)[i]
            return result_dict
        except Error as err:
            dprint(err)
            return None

    @staticmethod
    def get_all_aliases(db_cursor):
        # Output Format: [(name, alias), (name, alias), ...]
        get_plugin_query = f"""SELECT aliases.alias_id, aliases.name FROM aliases"""
        try:
            db_cursor.execute(get_plugin_query)
            result_list = []
            result_row = db_cursor.fetchall()
            if result_row is None:
                return None
            for i, item in enumerate(result_row):
                alias_data = GetDB.get_alias(db_cursor=db_cursor, alias_id=list(result_row)[i][0])
                result_list.append((alias_data['name'], alias_data['alias']))
            return result_list
        except Error as err:
            dprint(err)
            return None

    @staticmethod
    def get_plugin_help(db_cursor, plugin_id: int = None, plugin_name: str = None) -> str:
        # Output Format: str
        if plugin_id is None and plugin_name is None:
            return None
        get_plugin_help_query = ""
        if plugin_id:
            get_plugin_help_query = f"""
                        SELECT plugins_help.help_text
                        FROM plugins, plugins_help
                        WHERE plugins.plugin_id = ?
                        AND plugins_help.plugin_id = plugins.plugin_id;
                    """
        elif plugin_name:
            get_plugin_help_query = f"""
                        SELECT plugins_help.help_text
                        FROM plugins, plugins_help
                        WHERE plugins.name = ?
                        AND plugins_help.plugin_id = plugins.plugin_id;
                    """
        try:
            db_cursor.execute(get_plugin_help_query, (plugin_id if plugin_id is not None else plugin_name, ))
            result_row = db_cursor.fetchone()
            if result_row is None:
                return None
            return result_row[0]
        except Error as err:
            dprint(err)
            return None

    @staticmethod
    def get_all_plugin_help(db_cursor):
        # Output Format: List[str]
        get_plugin_help_query = f"""
                            SELECT plugins.name, plugins_help.help_text
                            FROM plugins, plugins_help
                            WHERE plugins.plugin_id = plugins_help.plugin_id;
                        """
        try:
            db_cursor.execute(get_plugin_help_query)
            result_dict = {}
            result_row = db_cursor.fetchall()
            if result_row is None:
                return None
            for i, item in enumerate(result_row):
                result_dict[list(result_row)[i][0]] = GetDB.get_plugin_data(db_cursor=db_cursor,
                                                                            plugin_name=list(result_row)[i][0])
            return result_dict
        except Error as err:
            dprint(err)
            return None

    @staticmethod
    def get_plugin_data(db_cursor, plugin_id: int = None, plugin_name: str = None):
        # Output Format: [(command_name, level), (command_name, level), ...]
        if plugin_id is None and plugin_name is None:
            return None
        get_plugin_query = ""
        if plugin_id:
            get_plugin_query = f"""
                SELECT plugins.name, commands.name, commands.level, permission_levels.level_type
                FROM plugins, commands, permission_levels
                WHERE plugins.plugin_id = ?
                AND plugins.plugin_id = commands.plugin_id
                AND commands.level = permission_levels.level_id
            """
        elif plugin_name:
            get_plugin_query = f"""
                SELECT commands.name, commands.level
                FROM plugins, commands, permission_levels
                WHERE plugins.name = ?
                AND plugins.plugin_id = commands.plugin_id
                AND commands.level = permission_levels.level_id
            """
        try:
            db_cursor.execute(get_plugin_query, (plugin_id if plugin_id is not None else plugin_name, ))
            result_list = []
            result_row = db_cursor.fetchall()
            if result_row is None:
                return None
            for i, item in enumerate(result_row):
                result_list.append((list(result_row)[i][0], list(result_row)[i][1]))
            return result_list
        except Error as err:
            dprint(err)
            return None

    @staticmethod
    def get_all_plugin_data(db_cursor):
        # Output Format: { plugin_name: [(command_name, level), (command_name, level)], plugin_name: ...}
        get_plugin_query = f"""
                    SELECT plugins.name, commands.name, commands.level
                    FROM plugins, commands, permission_levels
                    WHERE plugins.plugin_id = commands.plugin_id
                    AND commands.level = permission_levels.level_id
                """
        try:
            db_cursor.execute(get_plugin_query)
            result_dict = {}
            result_row = db_cursor.fetchall()
            if result_row is None:
                return None
            for i, item in enumerate(result_row):
                result_dict[list(result_row)[i][0]] = GetDB.get_plugin_data(db_cursor=db_cursor,
                                                                            plugin_name=list(result_row)[i][0])
            return result_dict
        except Error as err:
            dprint(err)
            return None


class UpdateDB:
    @staticmethod
    def update_user_privileges(db_conn, user_name, level, ignore_file_save=False) -> bool:
        update_privileges_query = f"""
            UPDATE permissions
            SET level = ?
            WHERE user_id = (SELECT users.user_id FROM users WHERE users.name = ? LIMIT 1)
            AND ? = (SELECT permission_levels.level_id FROM permission_levels WHERE permission_levels.level_id = ?);
        """
        try:
            db_conn.cursor().execute(update_privileges_query, (level, user_name, level, level))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Updated user permission in the database: {user_name}-{level}",
                       origin=L_DATABASE)
                log(INFO, f"Updated user permission in the database: {user_name}-{level}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def update_plugin_help(db_conn, plugin_name, plugin_help_text, ignore_file_save=False) -> bool:
        update_help_query = f"""
            UPDATE plugins_help
            SET help_text = ?
            WHERE plugin_id = (SELECT plugins.plugin_id from plugins WHERE plugins.name = ? );
        """
        try:
            db_conn.cursor().execute(update_help_query, (plugin_help_text, plugin_name))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Updated plugin help text in the database: {plugin_name}",
                       origin=L_DATABASE)
                log(INFO, f"Updated plugin help text in the database: {plugin_name}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False

    @staticmethod
    def update_alias(db_conn, alias_name, commands, ignore_file_save=False) -> bool:
        update_alias_query = f"""
            UPDATE aliases
            SET alias = ?
            WHERE name = ?;
        """
        try:
            db_conn.cursor().execute(update_alias_query, (commands, alias_name))
            save_memory_db(db_conn)
            if not ignore_file_save:
                save_memory_db_to_file()
            if db_conn.cursor().rowcount == -1:
                dprint(f"Updated alias in the database: {alias_name}",
                       origin=L_DATABASE)
                log(INFO, f"Updated alias in the database: {alias_name}",
                    origin=L_DATABASE)
                return True
            return False
        except Error as err:
            dprint(err)
            return False


class UtilityDB:
    @staticmethod
    def import_privileges_to_db(db_conn, csv_path):
        plugin_name = csv_path.split('/')[-2]
        # InsertDB.insert_new_plugin(db_conn, plugin_name=plugin_name)
        with open(csv_path, mode='r') as csv_file:
            csvr = DictReader(csv_file)
            for i, row in enumerate(csvr):
                try:
                    InsertDB.insert_new_command(db_conn, plugin_name=plugin_name, command_name=row['command'],
                                                permission_level=int(row['level']), ignore_file_save=True)
                except Error:
                    dprint("Encountered an error while importing plugin privileges data into the database.")
                    log(WARNING, "Encountered an error while importing plugin privileges data into the database.",
                        origin=L_DATABASE)
                    continue

    @staticmethod
    def import_aliases_to_db(db_conn, csv_path):
        file_name = csv_path.split('/')[-2]
        with open(csv_path, mode='r') as csv_file:
            csvr = DictReader(csv_file)
            for i, row in enumerate(csvr):
                try:
                    InsertDB.insert_new_alias(db_conn, alias_name=row['alias'].strip(), commands=row['command'].strip(), ignore_file_save=True)
                except Error:
                    dprint(
                        f"Encountered an error while importing a plugin alias from {file_name} plugin into the database.")
                    log(WARNING,
                        "Encountered an error while importing a plugin alias from {file_name} plugin into the database.",
                        origin=L_DATABASE)
                    continue

    @staticmethod
    def import_help_to_db(db_conn, html_path) -> bool:
        file_name = html_path.split('/')[-2]
        with open(html_path, mode='r') as html_file:
            try:
                file_content = html_file.read()
                InsertDB.insert_new_plugins_help(db_conn, plugin_name=file_name, help_text=html_file.read(), ignore_file_save=True)
                UpdateDB.update_plugin_help(db_conn, plugin_name=file_name, plugin_help_text=file_content)
                return True
            except Error:
                dprint("Encountered an error while importing plugin help data into the database.")
                log(WARNING, "Encountered an error while importing plugin help data into the database.",
                    origin=L_DATABASE)
                return False
