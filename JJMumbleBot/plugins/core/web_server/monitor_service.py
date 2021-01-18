from datetime import timedelta
import platform
import hashlib
import json
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.runtime_utils import get_all_channels
from JJMumbleBot.lib.helpers.image_helper import format_image
from copy import deepcopy


def get_all_socket_data():
    hasher = hashlib.md5()
    socket_data = {}
    socket_data.update(get_last_command_output())
    socket_data.update(get_all_online())
    socket_data.update(get_audio_info())
    socket_data.update(get_server_hierarchy())

    encoded_dict = json.dumps(dict(socket_data), sort_keys=True).encode()
    hasher.update(encoded_dict)
    socket_data.update({"hash": hasher.hexdigest()})
    return dict(socket_data)


def get_audio_info():
    hasher = hashlib.md5()
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

    encoded_dict = json.dumps(modified_audio_data, sort_keys=True).encode()
    hasher.update(encoded_dict)
    modified_audio_data["audio_data"]["hash"] = hasher.hexdigest()
    return modified_audio_data


def get_all_users():
    return {
        "users_count": global_settings.mumble_inst.users.count(),
        "all_users": global_settings.mumble_inst.users
    }


def get_all_online():
    hasher = hashlib.md5()
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
                f'channel_id': f'{user["channel_id"]}',
                f'channel_name': f'{all_channels_dict[channel_id]["name"]}'
            }

    # Remove description_hash key if inside any channel data.
    # Also add parent key and set to -1 if a parent key doesn't exist.
    for channel_id in all_channels_dict:
        if "description_hash" in all_channels_dict[channel_id]:
            del all_channels_dict[channel_id]["description_hash"]
        if "parent" not in all_channels_dict[channel_id]:
            all_channels_dict[channel_id]["parent"] = -1

    online_user_info["channels"] = all_channels_dict
    online_user_info["users"] = users_in_channels

    encoded_dict = json.dumps(online_user_info, sort_keys=True).encode()
    hasher.update(encoded_dict)
    online_user_info["hash"] = hasher.hexdigest()
    return {"server_info": online_user_info}


def get_server_hierarchy():
    hasher = hashlib.md5()
    server = []

    # Get all the channel dictionaries: format => {channel_id: 0, name: "Channel Name", position:-1, max_users:-1}
    all_channels = get_all_channels()
    # Iterate through the channel dictionary list and remove "description_hash" key if it exists.
    # If a "parent" key does not exist, add it with the value of -1
    for channel_id in all_channels:
        if "description_hash" in all_channels[channel_id]:
            del all_channels[channel_id]["description_hash"]
        if "parent" not in all_channels[channel_id]:
            all_channels[channel_id]["parent"] = -1

    # Iterate through all the channel dictionaries and create channel_info dictionaries with only the required info.
    channels_list = []
    for channel_id in all_channels:
        channel_info = {
            "channel_id": channel_id,
            "channel_name": all_channels[channel_id]["name"],
            "parent": all_channels[channel_id]["parent"],
            "users": [],
            "subchannels": []
        }
        # Set the users in every channel into the channel_info dictionary.
        for user in all_channels[channel_id].get_users():
            channel_info["users"].append(user["name"])
        # Append the channel_info dictionary to the server dictionary.
        channels_list.append(channel_info)

    # Organize the hierarchy of channels such that child channels are in the "subchannels" list.
    # The first channel in the list is always root.
    server.append(channels_list[0])

    # print(channels_list[1:])
    # The rest of the channels are either root, or have a parent.
    set_channel_data(server, channels_list[1:])

    encoded_dict = json.dumps(server, sort_keys=True).encode()
    hasher.update(encoded_dict)
    return {"server_hierarchy": {"hierarchy": server, "hash": hasher.hexdigest()}}


def set_channel_data(prev_tier_list, channels_list):
    # print(prev_tier_list)
    # Iterate through every channel in this tier...
    to_remove = []
    for channel in prev_tier_list:
        for i, cur_channel in enumerate(channels_list):
            # If the channel_id is the same as the current channel item parent...
            if channel["channel_id"] == cur_channel["parent"]:
                # Append the current channel item as a subchannel and remove it from the list...
                channel["subchannels"].append(cur_channel)
                to_remove.append(i)
    for index in sorted(to_remove, reverse=True):
        del channels_list[index]

    for channel in prev_tier_list:
        set_channel_data(channel["subchannels"], channels_list)


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
