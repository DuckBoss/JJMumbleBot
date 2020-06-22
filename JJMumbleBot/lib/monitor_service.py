import psutil
import platform
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.runtime_utils import get_all_channels


def get_all_users():
    return {
        "users_count": global_settings.mumble_inst.users.count(),
        "all_users": global_settings.mumble_inst.users
    }


def get_all_online():
    online_user_info = {
        "channels": {},
        "users": {}
    }
    all_channels_dict = get_all_channels()

    users_in_channels = {}
    for channel_id in all_channels_dict:
        all_users_in_channel = all_channels_dict[channel_id].get_users()
        users_in_channels[channel_id] = {}
        for user in all_users_in_channel:
            users_in_channels[channel_id][user["name"]] = {
                f'name': f'{user["name"]}',
                f'user_id': f'{user["user_id"]}',
                f'channel_id': f'{user["channel_id"]}'
            }

    online_user_info["channels"] = all_channels_dict
    online_user_info["users"] = users_in_channels
    return online_user_info


def get_hardware_info():
    return {
        "cpu_usage": f'{psutil.cpu_percent()}%',
        "mem_usage": f'{psutil.virtual_memory().percent}%'
    }


def get_last_command_output():
    return {
        "last_cmd_type": f'{global_settings.last_command_type}',
        "last_cmd_output": f'{global_settings.last_command_output}'
    }


def get_system_info():
    uname = platform.uname()
    return {
        "system": f'{uname.system}',
        "version": f'{uname.version}',
        "release": f'{uname.release}',
        "machine": f'{uname.machine}',
        "processor": f'{uname.processor}'
    }
