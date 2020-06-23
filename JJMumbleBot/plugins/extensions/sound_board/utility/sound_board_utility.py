from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.print_utils import dprint, rprint
from JJMumbleBot.plugins.extensions.sound_board.resources.strings import *
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.resources.strings import C_PLUGIN_SETTINGS
from JJMumbleBot.plugins.extensions.sound_board.utility import settings
from JJMumbleBot.lib.utils import runtime_utils
import os
import wave
import youtube_dl
import time
import audioop
import subprocess as sp


def prepare_sb_list():
    file_counter = 0
    gather_list = []
    for file_item in os.listdir(f"{dir_utils.get_perm_med_dir()}/sound_board/"):
        if file_item.endswith(".wav"):
            gather_list.append(f"{file_item}")
            file_counter += 1

    gather_list.sort(key=str.lower)
    return gather_list


def download_clip(url, name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': dir_utils.get_perm_med_dir() + f'/sound_board/{name}.wav',
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
    except Exception:
        return False


def play_audio():
    if global_settings.audio_dni[1] == settings.sound_board_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and global_settings.audio_dni[0] is True:
        global_settings.audio_dni = (True, settings.sound_board_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        global_settings.mumble_inst.sound_output.clear_buffer()

        runtime_utils.unmute()
        while not settings.exit_flag and global_settings.vlc_inst:
            while global_settings.mumble_inst.sound_output.get_buffer_size() > 0.5 and not settings.exit_flag:
                time.sleep(0.01)
            if global_settings.vlc_inst:
                raw_music = global_settings.vlc_inst.stdout.read(1024)
                if raw_music and global_settings.vlc_inst:
                    global_settings.mumble_inst.sound_output.add_sound(audioop.mul(raw_music, 2, settings.volume))
                else:
                    return
            else:
                return
        return
