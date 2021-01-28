from JJMumbleBot.lib.utils import dir_utils
import configparser
from os import path


def create_ini(plugin_name: str, cfg_parser) -> bool:
    if not path.exists(f'{dir_utils.get_plugin_data_dir()}/{plugin_name}/'):
        return False
    with open(f'{dir_utils.get_plugin_data_dir()}/{plugin_name}/{plugin_name}.ini', 'w') as cfg_file:
        cfg_parser.write(cfg_file)
    return True


def get_ini(plugin_name) -> configparser.ConfigParser:
    if path.exists(f'{dir_utils.get_plugin_data_dir()}/{plugin_name}/{plugin_name}.ini'):
        cfg = configparser.ConfigParser()
        cfg.read(f'{dir_utils.get_plugin_data_dir()}/{plugin_name}/{plugin_name}.ini')
        return cfg
    return None


def delete_ini(plugin_name) -> bool:
    if path.exists(f'{dir_utils.get_plugin_data_dir()}/{plugin_name}/{plugin_name}.ini'):
        dir_utils.remove_file(f'{plugin_name}.ini', f'{dir_utils.get_plugin_data_dir()}/{plugin_name}/')
        return True
    return False
