from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.database_utils import GetDB
import configparser


class PluginUtilityService:
    @staticmethod
    def process_metadata(meta_path: str):
        cfg = configparser.ConfigParser()
        # print(f'{dir_utils.get_main_dir()}/{meta_path.split(".")[0]}/metadata.ini')
        cfg.read(f'{dir_utils.get_main_dir()}/{meta_path.split(".")[0]}/metadata.ini')
        return cfg

    @staticmethod
    def process_help(db_cursor, plugin_name: str):
        plugin_help_data = GetDB.get_plugin_help(db_cursor=db_cursor, plugin_name=plugin_name)
        if plugin_help_data:
            return plugin_help_data
        return None
