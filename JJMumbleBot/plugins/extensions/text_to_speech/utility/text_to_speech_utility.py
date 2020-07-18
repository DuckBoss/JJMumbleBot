from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.print_utils import dprint, rprint
from JJMumbleBot.plugins.extensions.text_to_speech.utility import settings
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import runtime_utils
from os import listdir
import wave
from time import sleep
import audioop
import requests
from subprocess import call
from json import loads, dumps


def prepare_tts_list():
    file_counter = 0
    gather_list = []
    for file_item in listdir(f"{dir_utils.get_perm_med_dir()}/{settings.plugin_name}/"):
        if file_item.endswith(".oga"):
            if file_item.startswith("_temp"):
                continue
            gather_list.append(f"{file_item}")
            file_counter += 1

    gather_list.sort(key=str.lower)
    return gather_list


def get_cur_audio_length():
    wav_file = wave.open(f"{dir_utils.get_perm_med_dir()}/{settings.plugin_name}/{settings.current_track}.oga", 'r')
    frames = wav_file.getnframes()
    rate = wav_file.getframerate()
    duration = frames / float(rate)
    wav_file.close()
    return duration


def download_clip(clip_name, voice, msg, directory=None):
    temp = {'text': msg, 'voice': voice}
    json_dump = dumps(temp)

    if directory is None:
        directory = f'{dir_utils.get_perm_med_dir()}'

    try:
        url = 'https://streamlabs.com/polly/speak'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        r = requests.post(url, data=json_dump, headers=headers)
        # print(r.status_code)
        if r.status_code == 200:
            resp = requests.get(loads(r.text)['speak_url'])
            # print(resp.status_code)
            if resp.status_code == 200:
                with open(f'{directory}/{settings.plugin_name}/{clip_name}.oga', 'wb') as f:
                    f.write(resp.content)
                uri = f'{directory}/{settings.plugin_name}/{clip_name}.oga'
                call(
                    [global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_PATH], uri] + ['-I', 'dummy', '--quiet',
                                                                                  '--one-instance', '--no-repeat',
                                                                                  '--sout',
                                                                                  '#transcode{acodec=wav, channels=2, samplerate=43000, '
                                                                                  'ab=192, threads=8}:std{access=file, mux=wav, '
                                                                                  f'dst={directory}/{settings.plugin_name}/{clip_name}.wav '
                                                                                  '}',
                                                                                  'vlc://quit'])
                return True
            dprint(f'Could not download clip: Response-{r.status_code}')
            return False
        dprint(f'Could not download clip: Response-{r.status_code}')
        return False
    except Exception as e:
        dprint(e)
        return False


def play_audio():
    if global_settings.audio_dni[1] == settings.tts_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and global_settings.audio_dni[0] is True:
        global_settings.mumble_inst.sound_output.clear_buffer()

        runtime_utils.unmute()
        while not settings.exit_flag and global_settings.vlc_inst:
            while global_settings.mumble_inst.sound_output.get_buffer_size() > 0.5 and not settings.exit_flag:
                sleep(0.01)
            if global_settings.vlc_inst:
                raw_music = global_settings.vlc_inst.stdout.read(1024)
                if raw_music and global_settings.vlc_inst:
                    global_settings.mumble_inst.sound_output.add_sound(audioop.mul(raw_music, 2, runtime_utils.get_volume()))
                else:
                    global_settings.vlc_interface.stop()
                    global_settings.audio_dni = (False, None)
                    global_settings.vlc_interface.toggle_repeat(repeat=False)
                    global_settings.vlc_interface.toggle_loop(loop=False)
                    global_settings.gui_service.quick_gui("Stopped text to speech audio.", text_type='header',
                                             box_align='left')
                    return
            else:
                return
