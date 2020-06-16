from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.radio.resources.strings import *
from JJMumbleBot.plugins.extensions.radio.utility import radio_utility, settings
import urllib.request
from itertools import cycle
import re
import struct


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        settings.radio_metadata = self.metadata
        settings.all_radio_links = loads(self.metadata.get(C_PLUGIN_SETTINGS, P_RADIO_LINKS))
        settings.volume = float(self.metadata[C_PLUGIN_SETTINGS][P_DEF_VOL])
        settings.radio_pool = cycle(settings.all_radio_links)
        settings.radio_link = next(settings.radio_pool)
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_DIR][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        radio_utility.clear_audio_thread()
        radio_utility.stop_audio()
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}')
        radio_utility.exit_flag = True
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def get_metadata(self):
        return settings.radio_metadata

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "rdefault":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if not GS.audio_dni[0]:
                GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
            else:
                if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                    rprint(
                        f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                    GS.gui_service.quick_gui(
                        "An audio plugin is using the audio thread with no interruption mode enabled.",
                        text_type='header',
                        box_align='left')
                    return
            radio_utility.stop_audio()
            settings.radio_pool = cycle(settings.all_radio_links)
            settings.radio_link = next(settings.radio_pool)
            radio_utility.play_audio()

        elif command == "rvolume" or command == "rv":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                GS.gui_service.quick_gui(f"Current radio volume: {settings.volume}",
                                         text_type='header', box_align='left')
                return
            if vol > 1 or vol < 0:
                GS.gui_service.quick_gui("Invalid Radio Volume Input: [0-1]",
                                         text_type='header', box_align='left')
                return
            settings.volume = vol
            GS.gui_service.quick_gui(f"Set radio volume to {settings.volume}",
                                     text_type='header', box_align='left')

        elif command == "rstop":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if settings.is_playing and GS.audio_dni is not None:
                if not GS.audio_dni[0]:
                    GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
                else:
                    if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                        rprint(
                            f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                        GS.gui_service.quick_gui(
                            "An audio plugin is using the audio thread with no interruption mode enabled.",
                            text_type='header',
                            box_align='left')
                        return
                radio_utility.stop_audio()
                GS.gui_service.quick_gui("Stopping radio audio thread...",
                                         text_type='header', box_align='left')
                settings.is_playing = False
                return

        elif command == "rnext":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if not GS.audio_dni[0]:
                GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
            else:
                if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                    rprint(
                        f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                    GS.gui_service.quick_gui(
                        "An audio plugin is using the audio thread with no interruption mode enabled.",
                        text_type='header',
                        box_align='left')
                    return
            radio_utility.stop_audio()
            settings.radio_link = next(settings.radio_pool)
            radio_utility.play_audio()

        elif command == "rnew":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if len(message_parse) < 2:
                return
            if not GS.audio_dni[0]:
                GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
            else:
                if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                    rprint(
                        f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                    GS.gui_service.quick_gui(
                        "An audio plugin is using the audio thread with no interruption mode enabled.",
                        text_type='header',
                        box_align='left')
                    return
            settings.radio_link = message_parse[1]
            radio_utility.play_audio()
            return

        elif command == "rsong":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if not settings.is_playing:
                return
            try:
                url = settings.radio_link  # radio stream
                encoding = 'utf-8'  # default: iso-8859-1 for mp3 and utf-8 for ogg streams
                request = urllib.request.Request(url, headers={'Icy-MetaData': 1})  # request metadata
                response = urllib.request.urlopen(request)
                dprint(response.headers)
                metaint = int(response.headers['icy-metaint'])
                for _ in range(10):  # # title may be empty initially, try several times
                    response.read(metaint)  # skip to metadata
                    metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
                    metadata = response.read(metadata_length).rstrip(b'\0')
                    # extract title from the metadata
                    m = re.search(br"StreamTitle='([^']*)';", metadata)
                    if m:
                        title = m.group(1)
                        if title:
                            # print(title.decode(encoding, errors='replace'))
                            GS.gui_service.quick_gui(f"<br>Current Song: {title.decode(encoding, errors='replace')}<br>{url}",
                                                     text_type='header', box_align='left')
                            break
                        else:
                            # print("No title found!")
                            GS.gui_service.quick_gui("Could not retrieve a song title from this stream.",
                                                     text_type='header', box_align='left')
                return
            except Exception:
                GS.gui_service.quick_gui("This stream does not support this feature.",
                                         text_type='header', box_align='left')
                return
