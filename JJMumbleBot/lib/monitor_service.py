import psutil
import platform
from JJMumbleBot.settings import global_settings


def get_all_users():
    return {
        "users_count": global_settings.mumble_inst.users.count(),
        "all_users": global_settings.mumble_inst.users
    }


def get_all_plugins():
    return {
        "plugin_names": [x for x in global_settings.bot_plugins.keys()]
    }


def get_hardware_info():
    return {
        "cpu_usage": f'{psutil.cpu_percent()}%',
        "mem_usage": f'{psutil.virtual_memory().percent}%'
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
