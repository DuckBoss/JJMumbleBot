from os import listdir, path, unlink, makedirs
from pathlib import Path
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.resources.strings import *


def get_main_dir():
    return Path(path.dirname(__file__)).parent.parent


def get_temp_med_dir():
    return global_settings.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]


def get_perm_med_dir():
    return global_settings.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]


def get_plugin_data_dir():
    return f'{get_main_dir()}/cfg/plugins'


def get_core_plugin_dir():
    return f'{get_main_dir()}/plugins/core'


def get_extension_plugin_dir():
    return f'{get_main_dir()}/plugins/extensions'


def clear_directory(d):
    for the_file in listdir(d):
        file_path = path.join(d, the_file)
        try:
            if path.isfile(file_path):
                unlink(file_path)
        except Exception as e:
            log(ERROR, f"Encountered an error trying to clear a directory: {e}",
                origin=L_COMMAND, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.REG_PRINT.value)


def find_file(file_name, directory_name):
    for the_file in listdir(directory_name):
        try:
            file_path = path.join(directory_name, the_file)
            if path.isfile(file_path):
                if the_file == file_name:
                    return file_path
        except Exception as e:
            log(ERROR, f"Encountered an error trying to find the '{file_name}' file: {e}",
                origin=L_COMMAND, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.REG_PRINT.value)


def remove_file(file_name, directory_name):
    for the_file in listdir(directory_name):
        try:
            file_path = path.join(directory_name, the_file)
            if path.isfile(file_path):
                if the_file == file_name:
                    unlink(file_path)
        except Exception as e:
            log(ERROR, f"Encountered an error trying to remove a file: {e}",
                origin=L_COMMAND, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.REG_PRINT.value)


def make_directory(d):
    if not path.exists(d):
        makedirs(d)
