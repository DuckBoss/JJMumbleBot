import audioop
import os
from time import sleep
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import runtime_utils as rutils
from threading import Thread
import subprocess as sp


def create_vlc_instance(uri: str, skipto: int = 0):
    global_settings.vlc_thread = Thread(
        target=create_vlc_thread,
        args=(
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PATH],
            uri,
            skipto,
            global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_VLC_QUIET, fallback=True),
            global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_VLC_STEREO, fallback=True),
        ),
        daemon=True
    )
    global_settings.vlc_thread.start()


def stop_vlc_instance():
    if global_settings.vlc_inst:
        global_settings.vlc_inst.terminate()
        global_settings.vlc_inst.kill()
        global_settings.vlc_inst = None
    if global_settings.vlc_thread:
        global_settings.vlc_thread.join()
        global_settings.vlc_thread = None


def create_vlc_thread(vlc_path: str, uri: str, skipto: int = 0, quiet: bool = True, stereo: bool = True):
    if uri == '':
        return

    '''
    thr_settings = {
        'vlc_path': vlc_path,
        'uri': uri,
        'skipto': skipto,
        'quiet': quiet,
        'stereo': stereo,
        'exit_flag': False
    }
    '''
    # while not thr_settings['exit_flag']:
    global_settings.mumble_inst.sound_output.clear_buffer()
    if global_settings.vlc_inst:
        pid = global_settings.vlc_inst.pid
        global_settings.vlc_inst.terminate()
        try:
            os.kill(pid, 0)
            global_settings.vlc_inst.kill()
            print("Forced kill")
        except OSError as e:
            print("Terminated gracefully")
        global_settings.vlc_inst = None

    if stereo:
        global_settings.vlc_inst = sp.Popen(
            [vlc_path, uri] + ['-I', 'dummy',
                               f'{"--quiet" if quiet else ""}',
                               '--one-instance',
                               f'--start-time={skipto}',
                               '--sout',
                               '#transcode{acodec=s16le, channels=2, '
                               'samplerate=48000, ab=192, threads=8}:std{access=file, '
                               'mux=wav, dst=-}',
                               'vlc://quit'],
            stdout=sp.PIPE, bufsize=1024)
    else:
        global_settings.vlc_inst = sp.Popen(
            [vlc_path, uri] + ['-I', 'dummy',
                               f'{"--quiet" if quiet else ""}',
                               '--one-instance',
                               f'--start-time={skipto}',
                               '--sout',
                               '#transcode{acodec=s16le, channels=2, '
                               'samplerate=24000, ab=192, threads=8}:std{access=file, '
                               'mux=wav, dst=-}',
                               'vlc://quit'],
            stdout=sp.PIPE, bufsize=1024)
    rutils.unmute()

    while not global_settings.vlc_interface.exit_flag and global_settings.vlc_inst:
        while global_settings.mumble_inst.sound_output.get_buffer_size() > 0.5 and not global_settings.vlc_interface.exit_flag:
            sleep(0.01)
        if global_settings.vlc_inst:
            raw_music = global_settings.vlc_inst.stdout.read(1024)
            if raw_music and global_settings.vlc_interface.status.is_playing():
                global_settings.mumble_inst.sound_output.add_sound(audioop.mul(raw_music, 2, global_settings.vlc_interface.status.get_volume()))
            else:
                if global_settings.vlc_interface.next_track():
                    # thr_settings['uri'] = global_settings.vlc_interface.status.get_track().uri
                    # thr_settings['skipto'] = 0
                    # break
                    create_vlc_thread(vlc_path=vlc_path, uri=global_settings.vlc_interface.status.get_track().uri, skipto=0, quiet=quiet, stereo=stereo)
                else:
                    # thr_settings['exit_flag'] = True
                    global_settings.vlc_interface.reset()
                return
        else:
            return
