import audioop
import os
from time import sleep
from JJMumbleBot.lib.utils.print_utils import dprint
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.lib.errors import AudioError
from threading import Thread
import subprocess as sp
from enum import Enum


class AudioLibrary(Enum):
    FFMPEG = 'ffmpeg'
    VLC = 'vlc'


def create_audio_instance(uri: str, audio_lib, skipto: int = 0):
    if audio_lib.value == AudioLibrary.VLC.value:
        audio_lib_path = global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PATH]
    elif audio_lib.value == AudioLibrary.FFMPEG.value:
        audio_lib_path = global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_FFMPEG_PATH]
    else:
        raise AudioError("Error: The audio library set for this audio instance is not a valid type!")
    global_settings.audio_thread = Thread(
        target=create_audio_thread,
        args=(
            audio_lib_path,
            audio_lib,
            uri,
            skipto,
            global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_AUDIO_LIB_QUIET, fallback=True),
            global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_USE_STEREO, fallback=True),
            True if audio_lib == AudioLibrary.VLC else False
        ),
        daemon=True
    )
    global_settings.audio_thread.start()


def stop_audio_instance():
    if global_settings.audio_inst:
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None
    if global_settings.audio_thread:
        global_settings.audio_thread.join()
        global_settings.audio_thread = None


def create_audio_thread(audio_lib_path: str, audio_lib_type, uri: str, skipto: int = 0, quiet: bool = True,
                        stereo: bool = True, use_reconnect=False):
    if uri == '':
        return

    global_settings.mumble_inst.sound_output.clear_buffer()
    if global_settings.audio_inst:
        pid = global_settings.audio_inst.pid
        global_settings.audio_inst.terminate()
        try:
            os.kill(pid, 0)
            global_settings.audio_inst.kill()
        except OSError as e:
            dprint(e)
        global_settings.audio_inst = None

    if audio_lib_type.value == AudioLibrary.FFMPEG.value:
        params = [audio_lib_path]
        if quiet:
            params.extend(["-loglevel", "quiet"])
        if use_reconnect:
            params.extend(["-reconnect", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "2"])
        params.extend(["-i", uri, "-ss", f"{skipto}", "-acodec", "pcm_s16le", "-f", "s16le",
                       "-ab", "192k", "-ac", "2"])
        if stereo:
            params.extend(["-ar", "48000", "-threads", "8", "-"])
        else:
            params.extend(["-ar", "24000", "-threads", "8", "-"])
    elif audio_lib_type.value == AudioLibrary.VLC.value:
        params = [audio_lib_path, uri, '-I', 'dummy']
        if quiet:
            params.extend(["--quiet"])
        params.extend(["--one-instance", f"--start-time={skipto}"])
        if stereo:
            params.extend(["--sout",
                       "#transcode{acodec=s16le, channels=2, samplerate=48000, ab=192, threads=8}:std{access=file, mux=wav, dst=-}"])
        else:
            params.extend(["--sout",
                       "#transcode{acodec=s16le, channels=2, samplerate=24000, ab=192, threads=8}:std{access=file, mux=wav, dst=-}"])
        params.extend(["vlc://quit"])
    else:
        return

    global_settings.audio_inst = sp.Popen(params, stdout=sp.PIPE, bufsize=1024)

    rutils.unmute()

    while not global_settings.aud_interface.exit_flag and global_settings.audio_inst:
        while global_settings.mumble_inst.sound_output.get_buffer_size() > 0.5 and not global_settings.aud_interface.exit_flag:
            sleep(0.01)
        if global_settings.audio_inst:
            raw_music = global_settings.audio_inst.stdout.read(1024)
            if raw_music and global_settings.aud_interface.status.is_playing():
                global_settings.mumble_inst.sound_output.add_sound(
                    audioop.mul(raw_music, 2, global_settings.aud_interface.status.get_volume()))
            else:
                if global_settings.aud_interface.next_track():
                    create_audio_thread(audio_lib_path=audio_lib_path, audio_lib_type=audio_lib_type,
                                        uri=global_settings.aud_interface.status.get_track().uri, skipto=0, quiet=quiet,
                                        stereo=stereo)
                else:
                    global_settings.aud_interface.reset()
                return
        else:
            return
