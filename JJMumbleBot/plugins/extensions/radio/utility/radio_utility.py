from JJMumbleBot.plugins.extensions.radio.utility import settings
from JJMumbleBot.plugins.extensions.radio.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import dprint, rprint
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils import runtime_utils
from JJMumbleBot.lib.resources.strings import *
import subprocess as sp
import audioop
import time


def stop_audio():
    if global_settings.audio_inst is not None and settings.is_playing:
        dprint("Stopping radio audio thread...")
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None
        settings.is_playing = False
        global_settings.audio_dni = (False, None)
        return True
    return False


def clear_audio_thread():
    if global_settings.audio_inst is not None:
        dprint("Clearing radio audio thread...")
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None
        return True
    return False


def play_audio():
    global_settings.audio_dni = (True, settings.radio_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
    global_settings.mumble_inst.sound_output.clear_buffer()

    uri = settings.radio_link
    command = settings.radio_metadata[C_PLUGIN_SETTINGS][P_VLC_DIR]

    if global_settings.audio_inst is not None:
        global_settings.audio_inst.terminate()
        global_settings.audio_inst.kill()
        global_settings.audio_inst = None

    settings.is_playing = True
    if global_settings.audio_inst is None:
        use_stereo = global_settings.cfg.getboolean(C_MAIN_SETTINGS, P_AUD_STEREO)
        if use_stereo:
            global_settings.audio_inst = sp.Popen(
                [command, uri] + ['-I', 'dummy',
                                  f'{"--quiet" if settings.radio_metadata.getboolean(C_PLUGIN_SETTINGS, P_VLC_QUIET, fallback=True) else ""}',
                                  '--one-instance',
                                  '--sout',
                                  '#transcode{acodec=s16le, channels=2, samplerate=48000, '
                                  'ab=128, threads=8}:std{access=file, mux=wav, dst=-}',
                                  'vlc://quit'],
                stdout=sp.PIPE, bufsize=1024)
        else:
            global_settings.audio_inst = sp.Popen(
                [command, uri] + ['-I', 'dummy',
                                  f'{"--quiet" if settings.radio_metadata.getboolean(C_PLUGIN_SETTINGS, P_VLC_QUIET, fallback=True) else ""}',
                                  '--one-instance',
                                  '--sout',
                                  '#transcode{acodec=s16le, channels=2, samplerate=24000, '
                                  'ab=128, threads=8}:std{access=file, mux=wav, dst=-}',
                                  'vlc://quit'],
                stdout=sp.PIPE, bufsize=1024)

    runtime_utils.unmute()
    global_settings.gui_service.quick_gui(f"The radio is now playing from: {settings.radio_link}",
                                          text_type='header',
                                          box_align='left')
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
