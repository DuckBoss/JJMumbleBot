from JJMumbleBot.lib.utils import runtime_utils
from JJMumbleBot.lib.helpers import runtime_helper
from JJMumbleBot.lib.monitor import monitor_data
import json


def get_cpu_percentage():
    cpu_usage = {
        "cpu": monitor_data.cpu_percent
    }
    return json.dumps(cpu_usage)


def get_ram_percentage():
    ram_usage = {
        "ram": monitor_data.ram_percent
    }
    return json.dumps(ram_usage)


def get_online_users():
    users = {
        "users": monitor_data.online_users
    }
    return json.dumps(users)


def get_whisper_data_json():
    whisp_data = runtime_utils.get_whisper_clients_by_type(runtime_helper.whisper_target['type'])
    whisper_data = {
        "data": whisp_data
    }
    return json.dumps(whisper_data)


def get_channel_users_json():
    return json.dumps({"users": runtime_utils.get_users_in_my_channel()})


def get_bot_info_json():
    info = [runtime_utils.get_bot_name(), runtime_utils.get_version(), runtime_utils.get_about()]
    return json.dumps(info)


def get_bot_version_json():
    return json.dumps({runtime_utils.get_version()})


def get_bot_name_json():
    return json.dumps({runtime_utils.get_bot_name()})


def get_bot_channel_json():
    return json.dumps({runtime_utils.get_my_channel()})


def get_uptime_json():
    return json.dumps({"uptime": runtime_utils.check_up_time()})
