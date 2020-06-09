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


def stop_audio():
    if global_settings.audio_inst is not None and settings.is_playing:
        dprint("Stopping sound_board audio thread...")
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None
        settings.current_track = None
        global_settings.audio_dni = (False, None)
        return True
    return False


def get_cur_audio_length():
    wav_file = wave.open(f"{dir_utils.get_perm_med_dir()}/sound_board/{settings.current_track}.wav", 'r')
    frames = wav_file.getnframes()
    rate = wav_file.getframerate()
    duration = frames / float(rate)
    wav_file.close()
    return duration


def get_audio_length(file_name):
    try:
        wav_file = wave.open(f"{dir_utils.get_perm_med_dir()}/sound_board/{file_name}.wav", 'r')
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        wav_file.close()
        if not duration:
            return -1
    except Exception:
        return -1
    return duration


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


def clear_audio_thread():
    if global_settings.audio_inst is not None:
        dprint("Clearing sound_board audio thread...")
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None
        return True
    return False


def play_audio(loop=False):
    global_settings.audio_dni = (True, settings.sound_board_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
    global_settings.mumble_inst.sound_output.clear_buffer()

    uri = f"file:///{dir_utils.get_perm_med_dir()}/sound_board/{settings.current_track}.wav"
    command = settings.sound_board_metadata[C_PLUGIN_SETTINGS][P_VLC_DIR]

    if global_settings.audio_inst is not None:
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None

    settings.is_playing = True
    if global_settings.audio_inst is None:
        use_stereo = global_settings.cfg.getboolean(C_MAIN_SETTINGS, P_AUD_STEREO)
        if use_stereo:
            global_settings.audio_inst = sp.Popen(
                [command, uri] + ['-I', 'dummy', f'{"--quiet" if settings.sound_board_metadata.getboolean(C_PLUGIN_SETTINGS, P_VLC_QUIET, fallback=True) else ""}', '--one-instance', f'{"--no-repeat" if loop is False else "--repeat"}', '--sout',
                                  '#transcode{acodec=s16le, channels=2, samplerate=48000, '
                                  'ab=128, threads=8}:std{access=file, mux=wav, dst=-}',
                                  'vlc://quit'],
                stdout=sp.PIPE, bufsize=1024)
        else:
            global_settings.audio_inst = sp.Popen(
            [command, uri] + ['-I', 'dummy', f'{"--quiet" if settings.sound_board_metadata.getboolean(C_PLUGIN_SETTINGS, P_VLC_QUIET, fallback=True) else ""}', '--one-instance', f'{"--no-repeat" if loop is False else "--repeat"}', '--sout',
                              '#transcode{acodec=s16le, channels=2, samplerate=24000, '
                              'ab=128, threads=8}:std{access=file, mux=wav, dst=-}',
                              'vlc://quit'],
            stdout=sp.PIPE, bufsize=1024)

    runtime_utils.unmute()
    while not settings.exit_flag and global_settings.audio_inst and settings.is_playing:
        while global_settings.mumble_inst.sound_output.get_buffer_size() > 0.5 and not settings.exit_flag:
            time.sleep(0.01)
        if global_settings.audio_inst:
            raw_music = global_settings.audio_inst.stdout.read(1024)
            if raw_music and global_settings.audio_inst:
                global_settings.mumble_inst.sound_output.add_sound(audioop.mul(raw_music, 2, settings.volume))
            else:
                stop_audio()
                settings.is_playing = False
                return
        else:
            return
    return
