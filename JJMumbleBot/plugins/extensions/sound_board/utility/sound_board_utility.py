from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.plugins.extensions.sound_board.utility import settings
import os
import youtube_dl


def prepare_sb_list():
    file_counter = 0
    gather_list = []
    for file_item in os.listdir(f"{dir_utils.get_perm_med_dir()}/{settings.plugin_name}/"):
        if file_item.endswith(".wav"):
            gather_list.append(f"{file_item}")
            file_counter += 1
    gather_list.sort(key=str.lower)
    return gather_list


def download_clip(url, name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{dir_utils.get_perm_med_dir()}/{settings.plugin_name}/{name}.wav',
        'noplaylist': True,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192', }]
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            ydl.prepare_filename(info_dict)
            ydl.download([url])
            return True
    except youtube_dl.DownloadError:
        return False
