from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.dir_utils import get_main_dir
import sqlite3
from io import StringIO


def get_memory_db():
    global_settings.mumble_db_string.seek(0)
    temp_conn = sqlite3.connect(":memory:")
    temp_conn.executescript(global_settings.mumble_db_string.read())
    temp_conn.commit()
    temp_conn.row_factory = sqlite3.Row
    return temp_conn


def save_memory_db(mem_db_conn):
    temp_file = StringIO()
    for line in mem_db_conn.iterdump():
        temp_file.write("%s\n" % line)
    # mem_db_conn.close()
    global_settings.mumble_db_string = temp_file
    # print(global_settings.mumble_db_string.getvalue())


def save_memory_db_to_file():
    temp_conn = get_memory_db()
    with sqlite3.connect(f'{get_main_dir()}/cfg/jjmumblebot.db') as new_db:
        temp_conn.backup(new_db)
    # temp_conn.close()
