import audioop
import os
from time import sleep
from JJMumbleBot.lib.utils.print_utils import dprint
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import runtime_utils as rutils
from threading import Thread
import subprocess as sp


def create_audio_instance(uri: str, skipto: int = 0):
    global_settings.audio_thread = Thread(
        target=create_audio_thread,
        args=(
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_FFMPEG_PATH],
            uri,
            skipto,
            global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_FFMPEG_QUIET, fallback=True),
            global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_USE_STEREO, fallback=True),
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


def create_audio_thread(ffmpeg_path: str, uri: str, skipto: int = 0, quiet: bool = True, stereo: bool = True):
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

    if stereo:
        if quiet:
            global_settings.audio_inst = sp.Popen(
                [ffmpeg_path, "-loglevel", "quiet", "-i", uri, "-ss", f"{skipto}", "-acodec", "pcm_s16le", "-f", "s16le",
                 "-ab", "192k", "-ac", "2", "-ar", "48000", "-threads", "8", "-"],
                stdout=sp.PIPE, bufsize=1024
            )
        else:
            global_settings.audio_inst = sp.Popen(
                [ffmpeg_path, "-i", uri, "-ss", f"{skipto}", "-acodec", "pcm_s16le", "-f",
                 "s16le",
                 "-ab", "192k", "-ac", "2", "-ar", "48000", "-threads", "8", "-"],
                stdout=sp.PIPE, bufsize=1024
            )
    else:
        if quiet:
            global_settings.audio_inst = sp.Popen(
                [ffmpeg_path, "-loglevel quiet", "-i", uri, "-ss", f"{skipto}", "-acodec", "pcm_s16le", "-f", "s16le",
                 "-ab", "192k", "-ac", "2", "-ar", "24000", "-threads", "8", "-"],
                stdout=sp.PIPE, bufsize=1024
            )
        else:
            global_settings.audio_inst = sp.Popen(
                [ffmpeg_path, "-i", uri, "-ss", f"{skipto}", "-acodec", "pcm_s16le", "-f",
                 "s16le",
                 "-ab", "192k", "-ac", "2", "-ar", "24000", "-threads", "8", "-"],
                stdout=sp.PIPE, bufsize=1024
            )
    rutils.unmute()

    while not global_settings.aud_interface.exit_flag and global_settings.audio_inst:
        while global_settings.mumble_inst.sound_output.get_buffer_size() > 0.5 and not global_settings.aud_interface.exit_flag:
            sleep(0.01)
        if global_settings.audio_inst:
            raw_music = global_settings.audio_inst.stdout.read(1024)
            if raw_music and global_settings.aud_interface.status.is_playing():
                global_settings.mumble_inst.sound_output.add_sound(audioop.mul(raw_music, 2, global_settings.aud_interface.status.get_volume()))
            else:
                if global_settings.aud_interface.next_track():
                    create_audio_thread(ffmpeg_path=ffmpeg_path, uri=global_settings.aud_interface.status.get_track().uri, skipto=0, quiet=quiet, stereo=stereo)
                else:
                    global_settings.aud_interface.reset()
                return
        else:
            return
