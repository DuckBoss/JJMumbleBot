from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.print_utils import dprint
from JJMumbleBot.plugins.extensions.text_to_speech.utility import settings
from os import listdir
import requests
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


def download_clip(clip_name, voice, msg, directory=None):
    temp = {'text': msg, 'voice': voice}
    json_dump = dumps(temp)

    if directory is None:
        directory = f'{dir_utils.get_perm_med_dir()}'

    try:
        url = 'https://streamlabs.com/polly/speak'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        r = requests.post(url, data=json_dump, headers=headers)
        if r.status_code == 200:
            resp = requests.get(loads(r.text)['speak_url'])
            if resp.status_code == 200:
                with open(f'{directory}/{settings.plugin_name}/{clip_name}.oga', 'wb') as f:
                    f.write(resp.content)
                return True
            dprint(f'Could not download clip: Response-{r.status_code}')
            return False
        dprint(f'Could not download clip: Response-{r.status_code}')
        return False
    except Exception as e:
        dprint(e)
        return False
