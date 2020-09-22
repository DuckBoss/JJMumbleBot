from datetime import timedelta
import platform
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.runtime_utils import get_all_channels
from JJMumbleBot.lib.helpers.image_helper import format_image
from copy import deepcopy


def get_audio_info():
    global_settings.aud_interface.calculate_progress()
    copied_status = deepcopy(global_settings.aud_interface.status)
    modified_audio_data = {
        "audio_data": copied_status
    }

    modified_audio_data["audio_data"]["track"] = copied_status.get_track().to_dict()
    modified_audio_data["audio_data"]["status"] = copied_status.get_status().value
    modified_audio_data["audio_data"]["audio_library"] = ""

    if len(modified_audio_data["audio_data"]["img_uri_hashed"]) > 1:
        img_hashed_uri = modified_audio_data["audio_data"]["img_uri_hashed"]
        image_uri_split = modified_audio_data["audio_data"]["track"]["image_uri"].rsplit('/', 1)
        image_dir = image_uri_split[0]

        modified_audio_data["audio_data"]["img_uri_formatted"] = format_image(f"{img_hashed_uri}", "jpg", image_dir, size_goal=32768)
    else:
        modified_audio_data["audio_data"]["img_uri_formatted"] = ''
    modified_audio_data["audio_data"]["track"]["track_type"] = copied_status.get_track()["track_type"].value
    modified_audio_data["audio_data"]["volume"] = copied_status.get_volume()
    if int(modified_audio_data["audio_data"]["progress_time"]) > 0:
        modified_audio_data["audio_data"]["progress_string"] = str(
            timedelta(seconds=int(modified_audio_data["audio_data"]["progress_time"])))
        modified_audio_data["audio_data"]["duration_string"] = modified_audio_data["audio_data"]["track"]["duration"]
    else:
        modified_audio_data["audio_data"]["progress_string"] = 0
        modified_audio_data["audio_data"]["duration_string"] = modified_audio_data["audio_data"]["track"]["duration"]
    for i, track_item in enumerate(modified_audio_data["audio_data"]["queue"]):
        modified_audio_data["audio_data"]["queue"][i] = track_item.to_dict()
        modified_audio_data["audio_data"]["queue"][i]["track_type"] = modified_audio_data["audio_data"]["queue"][i]["track_type"].value
    return modified_audio_data


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
                f'channel_id': f'{user["channel_id"]}'
            }

    online_user_info["channels"] = all_channels_dict
    online_user_info["users"] = users_in_channels
    return online_user_info


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
