from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.utility import sound_board_utility as sbu
from JJMumbleBot.plugins.extensions.sound_board.utility import settings as sbu_settings
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name
from JJMumbleBot.lib.utils import dir_utils
import os
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        sbu_settings.sound_board_metadata = self.metadata
        sbu_settings.volume = float(self.metadata[C_PLUGIN_SETTINGS][P_DEF_VOL])
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        sbu.clear_audio_thread()
        sbu.stop_audio()
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}')
        sbu_settings.exit_flag = True
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def get_metadata(self):
        return self.metadata

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "sbstop":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
                if GS.vlc_interface.stop():
                    GS.audio_dni = (False, None)
                    GS.gui_service.quick_gui("Stopped sound board audio.", text_type='header',
                                             box_align='left')
            else:
                rprint(
                    f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                GS.gui_service.quick_gui(
                    "An audio plugin is using the audio thread with no interruption mode enabled.",
                    text_type='header',
                    box_align='left')

        elif command == "sbvolume":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                vol = float(message[1:].split(' ', 1)[-1])
            except IndexError:
                GS.gui_service.quick_gui(f"Current sound board volume: {sbu_settings.volume}", text_type='header',
                                         box_align='left')
                return
            if vol > 1 or vol < 0:
                GS.gui_service.quick_gui("Invalid sound_board volume Input: [0-1]", text_type='header',
                                         box_align='left')
                return
            sbu_settings.volume = vol
            log(INFO, f"Set {self.plugin_name} volume to {sbu_settings.volume}", origin=L_COMMAND)
            GS.gui_service.quick_gui(f"Set {self.plugin_name} volume to {sbu_settings.volume}", text_type='header',
                                     box_align='left')

        elif command == "sblist":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            internal_list = []
            gather_list = sbu.prepare_sb_list()
            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")
            cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local Sound Board Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local sound board files available."
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left',
                                         user=GS.mumble_inst.users[text.actor]['name'])
                log(INFO, "Displayed a list of all local sound board files.")
                return
            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                             user=GS.mumble_inst.users[text.actor]['name'])
                    cur_text = ""
            if cur_text != "":
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                         user=GS.mumble_inst.users[text.actor]['name'])
            log(INFO, "Displayed a list of all local sound board files.")

        elif command == "sblist_echo":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            internal_list = []
            gather_list = sbu.prepare_sb_list()

            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")
            cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local Sound Board Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local sound board files available."
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left')
                log(INFO, "Displayed a list of all local sound board files.")
                return
            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
                    cur_text = ""
            if cur_text != "":
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
            log(INFO, "Displayed a list of all local sound board files.")

        elif command == "sbdownload":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            all_messages = message[1:].split()
            all_messages_stripped = BeautifulSoup(message_parse[1], features='html.parser').get_text()
            split_msgs = all_messages_stripped.split()
            stripped_url = split_msgs[0]
            if len(all_messages) >= 3:
                if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
                    sbu.download_clip(stripped_url, split_msgs[1].strip())
                    GS.gui_service.quick_gui(f"Downloaded sound clip as : {split_msgs[1].strip()}.wav",
                                             text_type='header',
                                             box_align='left')
                    return
                return

        elif command == "sbdelete":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            all_messages = message[1:].split()
            if len(all_messages) == 2:
                if ".wav" in all_messages[1].strip():
                    dir_utils.remove_file(all_messages[1].strip(), f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/")
                    GS.gui_service.quick_gui(f"Deleted sound clip : {all_messages[1].strip()}", text_type='header',
                                             box_align='left')

        elif command == "sbplaying":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
                track_duration = int(GS.vlc_status.get_track_length())
                #track_duration = sbu.get_audio_length(sbu_settings.current_track)
                rprint(f'{get_bot_name()}({self.plugin_name}) is playing: {sbu_settings.current_track} (duration: {str(timedelta(seconds = round(track_duration))) if track_duration > 0 else "Unavailable"})', origin=L_COMMAND)
                GS.gui_service.quick_gui(
                    f'{get_bot_name()}({self.plugin_name}) is playing: {sbu_settings.current_track} (duration: {str(timedelta(seconds = round(track_duration))) if track_duration > 0 else "Unavailable"})',
                    text_type='header',
                    box_align='left')

        elif command == "sbrandom":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if GS.audio_dni[0] is False:
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
            # print(GS.audio_dni)
            gather_list = sbu.prepare_sb_list()

            random.seed(datetime.now())
            random_sfx = random.choice(gather_list)[:-4]

            if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{random_sfx}.wav"):
                GS.gui_service.quick_gui(
                    "The sound clip does not exist.",
                    text_type='header',
                    box_align='left')
                return False
            sbu_settings.current_track = random_sfx
            GS.vlc_interface.clear_playlist()
            GS.vlc_interface.add_to_playlist(mrl=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{random_sfx}.wav')
            GS.vlc_interface.play()
            sbu.play_audio()

        elif command == "sb":
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
            # print(GS.audio_dni)
            parameter = message_parse[1].strip()
            if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{parameter}.wav"):
                GS.gui_service.quick_gui(
                    "The sound clip does not exist.",
                    text_type='header',
                    box_align='left')
                return False
            sbu_settings.current_track = parameter
            GS.vlc_interface.clear_playlist()
            GS.vlc_interface.add_to_playlist(mrl=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{parameter}.wav')
            GS.vlc_interface.play()
            GS.gui_service.quick_gui(
                f"Playing sound clip: {sbu_settings.current_track}",
                text_type='header',
                box_align='left')
            sbu.play_audio()

        '''
        elif command == "sbseek":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if len(message_parse) < 2:
                return
            if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
                if not sbu_settings.loop_clip:
                    try:
                        seconds_to_skip = int(message_parse[1])
                        sbu_settings.skip_to = seconds_to_skip
                        sbu.play_audio()
                    except ValueError:
                        return
                else:
                    GS.gui_service.quick_gui(
                        f"The {self.plugin_name} seek feature is currently unavailable when looping clips.",
                        text_type='header',
                        box_align='left')
        '''