from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.utility import sound_board_utility as sbu
from JJMumbleBot.plugins.extensions.sound_board.utility import settings as sbu_settings
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name
from JJMumbleBot.lib.utils import dir_utils
from os import path
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        sbu_settings.sound_board_metadata = self.metadata
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
            if GS.vlc_interface.stop():
                GS.audio_dni = (False, None)
                GS.vlc_interface.toggle_repeat(repeat=False)
                GS.vlc_interface.toggle_loop(loop=False)
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}')
        sbu_settings.exit_flag = True
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def cmd_sbstop(self, data):
        if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
            if GS.vlc_interface.stop():
                GS.audio_dni = (False, None)
                GS.vlc_interface.toggle_repeat(repeat=False)
                GS.vlc_interface.toggle_loop(loop=False)
                GS.gui_service.quick_gui("Stopped sound board audio.", text_type='header',
                                         box_align='left')

    def cmd_sblist(self, data):
        internal_list = []
        data_actor = GS.mumble_inst.users[data.actor]
        gather_list = sbu.prepare_sb_list()
        for i, item in enumerate(gather_list):
            internal_list.append(
                f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")
        cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local Sound Board Files:</font>"
        if len(internal_list) == 0:
            cur_text += "<br>There are no local sound board files available."
            GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left',
                                     user=data_actor['name'])
            log(INFO, "Displayed a list of all local sound board files.")
            return
        for i, item in enumerate(internal_list):
            cur_text += item
            if i % 50 == 0 and i != 0:
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                         user=data_actor['name'])
                cur_text = ""
        if cur_text != "":
            GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                     user=data_actor['name'])
        log(INFO, "Displayed a list of all local sound board files.")

    def cmd_sblist_echo(self, data):
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

    def cmd_sbdownload(self, data):
        all_data = data.message.strip().split()
        url_stripped = BeautifulSoup(all_data[1], features='html.parser').get_text()
        if len(all_data) > 2:
            if "youtube.com" in url_stripped or "youtu.be" in url_stripped:
                sbu.download_clip(url_stripped, all_data[2].strip())
                GS.gui_service.quick_gui(f"Downloaded sound clip as : {all_data[2].strip()}.wav",
                                         text_type='header',
                                         box_align='left')
                return
            return

    def cmd_sbdelete(self, data):
        all_data = data.message().strip().split()
        if len(all_data) == 2:
            if ".wav" in all_data[1].strip():
                dir_utils.remove_file(all_data[1].strip(), f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/")
                GS.gui_service.quick_gui(f"Deleted sound clip : {all_data[1].strip()}", text_type='header',
                                         box_align='left')

    def cmd_sbplaying(self, data):
        if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
            track_duration = int(GS.vlc_status.get_track_length())
            rprint(
                f'{get_bot_name()}({self.plugin_name}) is playing: {sbu_settings.current_track} (duration: {str(timedelta(seconds=round(track_duration))) if track_duration > 0 else "Unavailable"})',
                origin=L_COMMAND)
            GS.gui_service.quick_gui(
                f'{get_bot_name()}({self.plugin_name}) is playing: {sbu_settings.current_track} (duration: {str(timedelta(seconds=round(track_duration))) if track_duration > 0 else "Unavailable"})',
                text_type='header',
                box_align='left')

    def cmd_sbrandom(self, data):
        if GS.audio_dni[0] is False:
            GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                rprint(
                    f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                GS.gui_service.quick_gui(
                    f"An audio plugin({GS.audio_dni[1]}) is using the audio thread with no interruption mode enabled.",
                    text_type='header',
                    box_align='left')
                return
        # print(GS.audio_dni)
        gather_list = sbu.prepare_sb_list()

        random.seed(datetime.now())
        random_sfx = random.choice(gather_list)[:-4]

        if not path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{random_sfx}.wav"):
            GS.gui_service.quick_gui(
                "The sound clip does not exist.",
                text_type='header',
                box_align='left')
            return False
        sbu_settings.current_track = random_sfx
        GS.vlc_interface.toggle_repeat(repeat=False)
        GS.vlc_interface.toggle_loop(loop=False)
        GS.vlc_interface.clear_playlist()
        GS.vlc_interface.add_and_play_to_playlist(
            mrl=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{random_sfx}.wav')
        sbu.play_audio()

    def cmd_sb(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return
        if not GS.audio_dni[0]:
            GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                rprint(
                    f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                GS.gui_service.quick_gui(
                    f"An audio plugin({GS.audio_dni[1]}) is using the audio thread with no interruption mode enabled.",
                    text_type='header',
                    box_align='left')
                return
        # print(GS.audio_dni)
        to_play = all_data[1].strip()
        if not path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav"):
            GS.gui_service.quick_gui(
                "The sound clip does not exist.",
                text_type='header',
                box_align='left')
            return False
        sbu_settings.current_track = to_play
        GS.vlc_interface.toggle_repeat(repeat=False)
        GS.vlc_interface.toggle_loop(loop=False)
        GS.vlc_interface.clear_playlist()
        GS.vlc_interface.add_and_play_to_playlist(
            mrl=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav')
        GS.gui_service.quick_gui(
            f"Playing sound clip: {sbu_settings.current_track}",
            text_type='header',
            box_align='left')
        sbu.play_audio()

    def cmd_sbquiet(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return
        if not GS.audio_dni[0]:
            GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                rprint(
                    f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                GS.gui_service.quick_gui(
                    f"An audio plugin({GS.audio_dni[1]}) is using the audio thread with no interruption mode enabled.",
                    text_type='header',
                    box_align='left')
                return
        # print(GS.audio_dni)
        to_play = all_data[1].strip()
        if not path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav"):
            GS.gui_service.quick_gui(
                "The sound clip does not exist.",
                text_type='header',
                box_align='left')
            return False
        sbu_settings.current_track = to_play
        GS.vlc_interface.toggle_repeat(repeat=False)
        GS.vlc_interface.toggle_loop(loop=False)
        GS.vlc_interface.clear_playlist()
        GS.vlc_interface.add_and_play_to_playlist(
            mrl=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav')
        sbu.play_audio()

    def cmd_sbloop(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return
        if not GS.audio_dni[0]:
            GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                rprint(
                    f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                GS.gui_service.quick_gui(
                    f"An audio plugin({GS.audio_dni[1]}) is using the audio thread with no interruption mode enabled.",
                    text_type='header',
                    box_align='left')
                return
        to_play = all_data[1].strip()
        if not path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav"):
            GS.gui_service.quick_gui(
                "The sound clip does not exist.",
                text_type='header',
                box_align='left')
            return False
        sbu_settings.current_track = to_play
        GS.vlc_interface.toggle_loop(loop=False)
        GS.vlc_interface.clear_playlist()
        GS.vlc_interface.add_and_play_to_playlist(
            mrl=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav')
        GS.vlc_interface.toggle_repeat(repeat=True)
        sbu.play_audio()
        GS.gui_service.quick_gui(
            f"Playing looping sound clip: {sbu_settings.current_track}",
            text_type='header',
            box_align='left')

    def cmd_sbloopquiet(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return
        if not GS.audio_dni[0]:
            GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                rprint(
                    f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                GS.gui_service.quick_gui(
                    f"An audio plugin({GS.audio_dni[1]}) is using the audio thread with no interruption mode enabled.",
                    text_type='header',
                    box_align='left')
                return
        to_play = all_data[1].strip()
        if not path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav"):
            GS.gui_service.quick_gui(
                "The sound clip does not exist.",
                text_type='header',
                box_align='left')
            return False
        sbu_settings.current_track = to_play
        GS.vlc_interface.toggle_loop(loop=False)
        GS.vlc_interface.clear_playlist()
        GS.vlc_interface.add_and_play_to_playlist(
            mrl=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav')
        GS.vlc_interface.toggle_repeat(repeat=True)
        sbu.play_audio()

    def cmd_sbseek(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return
        if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
            try:
                GS.vlc_interface.seek(int(all_data[1]))
                # sbu.play_audio()
            except ValueError:
                return
