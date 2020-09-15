import csv
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.plugins.extensions.server_tools.utility import settings


def read_user_connections():
    try:
        with open(f'{dir_utils.get_main_dir()}/plugins/extensions/{settings.plugin_name}/resources/user_connections.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                settings.user_connections[row['username']] = row['track']
        return True
    except IOError:
        return False


def save_user_connections():
    try:
        with open(f'{dir_utils.get_main_dir()}/plugins/extensions/{settings.plugin_name}/resources/user_connections.csv', mode='w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=['username', 'track'])
            csv_writer.writeheader()
            for user in settings.user_connections:
                csv_writer.writerow({'username': user, 'track': settings.user_connections[user]})
        return True
    except IOError:
        return False
