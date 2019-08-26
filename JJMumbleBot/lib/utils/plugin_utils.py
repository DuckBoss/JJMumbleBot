from JJMumbleBot.lib.utils import dir_utils
import configparser


class PluginUtilityService:
    @staticmethod
    def process_metadata(meta_path: str):
        cfg = configparser.ConfigParser()
        # print(f'{dir_utils.get_main_dir()}/{meta_path.split(".")[0]}/metadata.ini')
        cfg.read(f'{dir_utils.get_main_dir()}/{meta_path.split(".")[0]}/metadata.ini')
        return cfg

    # TODO: Implement this method
    @staticmethod
    def process_help(help_path: str):
        return help_path
