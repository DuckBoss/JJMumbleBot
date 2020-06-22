import psutil
import platform
from JJMumbleBot.settings import global_settings


def get_all_users():
    return {
        "users_count": global_settings.mumble_inst.users.count(),
        "all_users": global_settings.mumble_inst.users
    }


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
