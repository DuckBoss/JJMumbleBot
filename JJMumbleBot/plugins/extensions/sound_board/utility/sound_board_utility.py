from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.print_utils import dprint, rprint
from JJMumbleBot.plugins.extensions.sound_board.resources.strings import *
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.resources.strings import C_PLUGIN_SETTINGS
from JJMumbleBot.lib.utils import runtime_utils
import os
import wave
import youtube_dl
import time
import audioop
import subprocess as sp

exit_flag = False
current_track = None
is_playing = False
sound_board_metadata = None
# default volume
volume = 0.5


def prepare_sb_list():
    file_counter = 0
    gather_list = []
    for file_item in os.listdir(f"{dir_utils.get_perm_med_dir()}/sound_board/"):
        if file_item.endswith(".wav"):
            gather_list.append(f"{file_item}")
            file_counter += 1

    gather_list.sort(key=str.lower)
    return gather_list


def stop_audio():
    global current_track
    if global_settings.audio_inst is not None and is_playing:
        dprint("Stopping sound_board audio thread...")
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None
        current_track = None
        global_settings.audio_dni = (False, None)
        return True
    return False


def get_cur_audio_length():
    wav_file = wave.open(f"{dir_utils.get_perm_med_dir()}/sound_board/{current_track}.wav", 'r')
    frames = wav_file.getnframes()
    rate = wav_file.getframerate()
    duration = frames / float(rate)
    wav_file.close()
    return duration


def download_clip(url, name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': dir_utils.get_perm_med_dir() + f'sound_board/{name}.wav',
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


def clear_audio_thread():
    if global_settings.audio_inst is not None:
        dprint("Clearing sound_board audio thread...")
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None
        return True
    return False


def play_audio():
    global_settings.audio_dni = (True, sound_board_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
    global_settings.mumble_inst.sound_output.clear_buffer()

    uri = f"file:///{dir_utils.get_perm_med_dir()}/sound_board/{current_track}.wav"
    command = sound_board_metadata[C_PLUGIN_SETTINGS][P_VLC_DIR]

    if global_settings.audio_inst is not None:
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None

    global is_playing
    is_playing = True
    if global_settings.audio_inst is None:
        global_settings.audio_inst = sp.Popen(
            [command, uri] + ['-I', 'dummy', '--quiet', '--one-instance', '--no-repeat', '--sout',
                              '#transcode{acodec=s16le, channels=2, samplerate=24000, '
                              'ab=128, threads=8}:std{access=file, mux=wav, dst=-}',
                              'vlc://quit'],
            stdout=sp.PIPE, bufsize=480)

    runtime_utils.unmute()
    while not exit_flag and global_settings.audio_inst and is_playing:
        while global_settings.mumble_inst.sound_output.get_buffer_size() > 0.5 and not exit_flag:
            time.sleep(0.01)
        if global_settings.audio_inst:
            raw_music = global_settings.audio_inst.stdout.read(480)
            if raw_music and global_settings.audio_inst:
                global_settings.mumble_inst.sound_output.add_sound(audioop.mul(raw_music, 2, volume))
            else:
                stop_audio()
                is_playing = False
                return
        else:
            return
    return
