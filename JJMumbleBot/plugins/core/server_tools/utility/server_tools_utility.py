from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.plugins.core.server_tools.utility import settings
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.resources.strings import ERROR, L_COMMAND, GEN_PROCESS_ERR
from JJMumbleBot.lib.utils.print_utils import PrintMode
from os import path
import csv


def read_user_connections():
    try:
        if not path.exists(f'{dir_utils.get_plugin_data_dir()}/{settings.plugin_name}/'):
            dir_utils.make_directory(f'{dir_utils.get_plugin_data_dir()}/{settings.plugin_name}/')
            create_empty_user_connections()

        with open(f'{dir_utils.get_plugin_data_dir()}/{settings.plugin_name}/user_connections.csv', mode='r') as csv_file:
            settings.user_connections = {}
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                settings.user_connections[row['username']] = row['track']
        return True
    except IOError:
        log(ERROR, f"Encountered an error reading/writing the user_connections.csv file.",
            origin=L_COMMAND, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False


def save_user_connections():
    try:
        if not path.exists(f'{dir_utils.get_plugin_data_dir()}/{settings.plugin_name}/'):
            dir_utils.make_directory(f'{dir_utils.get_plugin_data_dir()}/{settings.plugin_name}/')

        with open(f'{dir_utils.get_plugin_data_dir()}/{settings.plugin_name}/user_connections.csv', mode='w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=['username', 'track'])
            csv_writer.writeheader()
            for user in settings.user_connections:
                csv_writer.writerow({'username': user, 'track': settings.user_connections[user]})
        return True
    except IOError:
        log(ERROR, f"Encountered an error reading/writing the user_connections.csv file.",
            origin=L_COMMAND, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False


def create_empty_user_connections():
    try:
        if not path.exists(f'{dir_utils.get_plugin_data_dir()}/{settings.plugin_name}/user_connections.csv'):
            with open(f'{dir_utils.get_plugin_data_dir()}/{settings.plugin_name}/user_connections.csv', mode='w') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=['username', 'track'])
                csv_writer.writeheader()
            settings.user_connections = {}
        return True
    except IOError:
        log(ERROR, f"Encountered an error reading/writing the user_connections.csv file.",
            origin=L_COMMAND, error_type=GEN_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
        return False
