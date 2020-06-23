from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *


def create_vlc_single_instance():
    from threading import Thread
    global_settings.vlc_thread = Thread(
        target=create_vlc_thread,
        args=(
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PATH],
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PASS],
            global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_VLC_STEREO, fallback=True)
        )
    )
    global_settings.vlc_thread.start()


def create_vlc_thread(vlc_path, interface_password, stereo=True):
    import subprocess as sp
    if stereo:
        global_settings.vlc_inst = sp.Popen(
            [vlc_path] + ['-I', 'http', '--http-password', f'{interface_password}',
                          '--quiet',
                          '--one-instance',
                          '--sout',
                          '#transcode{acodec=s16le, channels=2, '
                          'samplerate=48000, ab=192, threads=8}:std{access=file, '
                          'mux=wav, dst=-}'],
            stdout=sp.PIPE, bufsize=1024)
    else:
        global_settings.vlc_inst = sp.Popen(
            [vlc_path] + ['-I', 'http', '--http-password', f'{interface_password}',
                          '--quiet',
                          '--one-instance',
                          '--sout',
                          '#transcode{acodec=s16le, channels=2, '
                          'samplerate=24000, ab=192, threads=8}:std{access=file, '
                          'mux=wav, dst=-}'],
            stdout=sp.PIPE, bufsize=1024)