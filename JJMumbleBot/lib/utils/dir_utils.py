import os
from pathlib import Path
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *


def get_main_dir():
    return Path(os.path.dirname(__file__)).parent.parent


def get_temp_img_dir():
    return global_settings.cfg[C_MEDIA_DIR][P_TEMP_IMG_DIR]


def get_perm_med_dir():
    return global_settings.cfg[C_MEDIA_DIR][P_PERM_MEDIA_DIR]


def clear_directory(d):
    for the_file in os.listdir(d):
        file_path = os.path.join(d, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def remove_file(f, d):
    for the_file in os.listdir(d):
        try:
            file_path = os.path.join(d, the_file)
            if os.path.isfile(file_path):
                if the_file == f:
                    os.unlink(file_path)
        except Exception as e:
            print(e)


def make_directory(d):
    if not os.path.exists(d):
        os.makedirs(d)
