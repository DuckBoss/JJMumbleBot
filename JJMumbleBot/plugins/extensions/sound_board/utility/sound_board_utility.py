import datetime
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.plugins.extensions.sound_board.utility import settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.resources.strings import *
import os
import yt_dlp
import subprocess
from fuzzywuzzy import process


def prepare_sb_list(include_file_extensions=False):
    file_counter = 0
    gather_list = []
    for file_item in os.listdir(
        f"{dir_utils.get_perm_med_dir()}/{settings.plugin_name}/"
    ):
        if include_file_extensions:
            gather_list.append(file_item)
        else:
            file_name = file_item.rsplit(".", 1)[0]
            gather_list.append(file_name)
        file_counter += 1
    gather_list.sort(key=str.lower)
    return gather_list


def find_file(file_name):
    for file_item in os.listdir(
        f"{dir_utils.get_perm_med_dir()}/{settings.plugin_name}/"
    ):
        if file_item.rsplit(".", 1)[0] == file_name:
            return file_item
    return None


def find_files(query: str):
    file_list = [
        file_item.rsplit(".", 1)[0]
        for file_item in os.listdir(
            f"{dir_utils.get_perm_med_dir()}/{settings.plugin_name}/"
        )
    ]
    file_ratios = process.extract(query, file_list)
    match_list = []
    for file_item in file_ratios:
        if file_item[1] > int(
            settings.sound_board_metadata[C_PLUGIN_SET][P_FUZZY_SEARCH_THRESHOLD]
        ) and len(match_list) < int(
            settings.sound_board_metadata[C_PLUGIN_SET][P_MAX_SEARCH_RESULTS]
        ):
            match_list.append(file_item[0])
    return match_list


def download_clip(url, name, time_range=None, ffmpeg_path="ffmpeg", proxy=""):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{dir_utils.get_perm_med_dir()}/{settings.plugin_name}/{name}.webm",
        "noplaylist": True,
        "youtube_skip_dash_manifest": True,
        "proxy": proxy,
    }
    try:
        info_dict = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            if time_range:
                info_dict = ydl.extract_info(url, download=False)
            else:
                ydl.download([url])
        if time_range:
            epoch_time = datetime.datetime(1900, 1, 1)
            a_timedelta = (
                datetime.datetime.strptime(time_range[0], "%H:%M:%S") - epoch_time
            )
            start_seconds = a_timedelta.total_seconds()
            b_timedelta = (
                datetime.datetime.strptime(time_range[1], "%H:%M:%S") - epoch_time
            )
            end_seconds = b_timedelta.total_seconds()
            end_range = f"{datetime.timedelta(seconds=(end_seconds - start_seconds))}"
            subprocess.call(
                [
                    ffmpeg_path,
                    "-nostats",
                    "-hide_banner",
                    "-ss",
                    time_range[0],
                    "-i",
                    info_dict["url"],
                    "-to",
                    end_range,
                    "-c",
                    "copy",
                    f"{dir_utils.get_perm_med_dir()}/{settings.plugin_name}/{name}.ogg",
                ]
            )
        return True
    except yt_dlp.DownloadError:
        return False
