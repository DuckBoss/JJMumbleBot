from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.resources.strings import *
from threading import Thread
import vlc


def create_vlc_single_instance():
    global_settings.vlc_thread = Thread(
        target=create_vlc_thread,
        args=(
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PATH],
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_IP],
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PORT],
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PASS],
            global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_VLC_QUIET, fallback=True),
            global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_VLC_STEREO, fallback=True)
        ),
        daemon=True
    )
    global_settings.vlc_thread.start()


def stop_vlc_instance():
    if global_settings.vlc_inst:
        global_settings.vlc_inst.kill()
        global_settings.vlc_inst = None
    if global_settings.vlc_thread:
        global_settings.vlc_thread = None


def create_vlc_thread(vlc_path, intf_ip, intf_port, intf_pass, quiet=True, stereo=True):
    import subprocess as sp
    if stereo:
        global_settings.vlc_inst = sp.Popen(
            [vlc_path] + ['-I', 'http',
                          '--http-host', f'{intf_ip}',
                          '--http-port', f'{intf_port}',
                          '--http-password', f'{intf_pass}',
                          f'{"--quiet" if quiet else ""}',
                          '--one-instance',
                          '--sout',
                          '#transcode{acodec=s16le, channels=2, '
                          'samplerate=48000, ab=192, threads=8}:std{access=file, '
                          'mux=wav, dst=-}'],
            stdout=sp.PIPE, bufsize=1024)
    else:
        global_settings.vlc_inst = sp.Popen(
            [vlc_path] + ['-I', 'http',
                          '--http-host', f'{intf_ip}',
                          '--http-port', f'{intf_port}',
                          '--http-password', f'{intf_pass}',
                          f'{"--quiet" if quiet else ""}',
                          '--one-instance',
                          '--sout',
                          '#transcode{acodec=s16le, channels=2, '
                          'samplerate=24000, ab=192, threads=8}:std{access=file, '
                          'mux=wav, dst=-}'],
            stdout=sp.PIPE, bufsize=1024)
