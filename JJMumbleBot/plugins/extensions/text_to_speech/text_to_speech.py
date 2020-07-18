from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils.runtime_utils import get_command_token
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.text_to_speech.utility import text_to_speech_utility as ttsu
from JJMumbleBot.plugins.extensions.text_to_speech.utility import settings as tts_settings
from JJMumbleBot.plugins.extensions.text_to_speech.resources.strings import *
from JJMumbleBot.lib.utils import dir_utils
import os


class Plugin(PluginBase):
    def __init__(self):
        from json import loads
        super().__init__()
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        tts_settings.tts_metadata = self.metadata
        tts_settings.plugin_name = self.plugin_name
        tts_settings.voice_list = loads(self.metadata.get(C_PLUGIN_SETTINGS, P_TTS_ALL_VOICE))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
            if GS.vlc_interface.stop():
                GS.audio_dni = (False, None)
                GS.vlc_interface.toggle_repeat(repeat=False)
                GS.vlc_interface.toggle_loop(loop=False)
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/text_to_speech')
        tts_settings.exit_flag = True
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def cmd_ttsstop(self, data):
        if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
            if GS.vlc_interface.stop():
                GS.audio_dni = (False, None)
                GS.vlc_interface.toggle_repeat(repeat=False)
                GS.vlc_interface.toggle_loop(loop=False)
                GS.gui_service.quick_gui("Stopped text to speech audio.", text_type='header',
                                         box_align='left')

    def cmd_ttslist(self, data):
        data_actor = GS.mumble_inst.users[data.actor]
        internal_list = []
        gather_list = ttsu.prepare_tts_list()
        for i, item in enumerate(gather_list):
            internal_list.append(
                f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")
        cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local TTS Files:</font>"
        if len(internal_list) == 0:
            cur_text += "<br>There are no local text to speech files available."
            GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left',
                                     user=data_actor['name'])
            GS.log_service.info("Displayed a list of all local text to speech files.")
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
        log(INFO, "Displayed a list of all local text to speech files.", origin=L_COMMAND)

    def cmd_ttsvoices(self, data):
        if len(tts_settings.voice_list) == 0:
            cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Available Voices:</font> None"
            GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left')
            log(INFO, "Displayed a list of all available text to speech voices.", origin=L_COMMAND)
            return
        cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Available Voices:</font>"
        for i, voice_name in enumerate(tts_settings.voice_list):
            cur_text += f"[{i}] - {voice_name}<br>"
        GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left')
        log(INFO, "Displayed a list of all available text to speech voices.", origin=L_COMMAND)

    def cmd_ttsdownload(self, data):
        all_data = data.message.strip().split(' ', 3)
        if ttsu.download_clip(all_data[1].strip(), all_data[2].strip(), all_data[3].strip()):
            GS.gui_service.quick_gui(f"Downloaded text to speech clip as : {all_data[1].strip()}.oga",
                                     text_type='header',
                                     box_align='left')
            return

    def cmd_ttsdelete(self, data):
        all_data = data.message.strip().split(' ', 1)
        if ".oga" in all_data[1].strip():
            dir_utils.remove_file(all_data[1].strip(), f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/")
            GS.gui_service.quick_gui(f"Deleted text to speech clip : {all_data[1].strip()}",
                                     text_type='header',
                                     box_align='left')
            return
        return

    def cmd_ttsplay(self, data):
        all_data = data.message.strip().split(' ', 1)
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
        if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.oga"):
            GS.gui_service.quick_gui(
                "The text to speech clip does not exist.",
                text_type='header',
                box_align='left')
            return False
        tts_settings.current_track = to_play
        GS.vlc_interface.toggle_repeat(repeat=False)
        GS.vlc_interface.toggle_loop(loop=False)
        GS.vlc_interface.clear_playlist()
        GS.vlc_interface.add_and_play_to_playlist(
            mrl=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.oga')
        GS.gui_service.quick_gui(
            f"Playing text-to-speech clip: {tts_settings.current_track}",
            text_type='header',
            box_align='left')
        ttsu.play_audio()

    def cmd_ttsplayquiet(self, data):
        all_data = data.message.strip().split(' ', 1)
        if not GS.audio_dni[0]:
            GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                return
        to_play = all_data[1].strip()
        if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.oga"):
            return False
        tts_settings.current_track = to_play
        GS.vlc_interface.toggle_repeat(repeat=False)
        GS.vlc_interface.toggle_loop(loop=False)
        GS.vlc_interface.clear_playlist()
        GS.vlc_interface.add_and_play_to_playlist(
            mrl=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.oga')
        ttsu.play_audio()

    def cmd_tts(self, data):
        data_actor = GS.mumble_inst.users[data.actor]
        all_data = data.message.strip().split(' ', 2)
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

        if all_data[1].strip() in tts_settings.voice_list:
            all_data = data.message.strip().split(' ', 2)
        else:
            all_data = data.message.strip().split(' ', 1)

        if len(all_data) == 2:
            if len(all_data[1]) > int(self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]):
                GS.gui_service.quick_gui(
                    f"The text to speech message exceeded the character limit:"
                    f" [{self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]}].",
                    text_type='header',
                    box_align='left',
                    user=data_actor['name'])
                return
            if ttsu.download_clip("_temp",
                                  self.metadata[C_PLUGIN_SETTINGS][P_TTS_DEF_VOICE],
                                  all_data[1].strip(),
                                  directory=f'{dir_utils.get_temp_med_dir()}'
                                  ):
                tts_settings.current_track = "_temp"
                GS.vlc_interface.toggle_repeat(repeat=False)
                GS.vlc_interface.toggle_loop(loop=False)
                GS.vlc_interface.clear_playlist()
                GS.vlc_interface.add_and_play_to_playlist(
                    mrl=f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}/{tts_settings.current_track}.oga')
                ttsu.play_audio()
                return
        elif len(all_data) == 3:
            if len(all_data[1]) > int(self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]):
                GS.gui_service.quick_gui(
                    f"The text to speech message exceeded the character limit:"
                    f" [{self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]}].",
                    text_type='header',
                    box_align='left',
                    user=data_actor['name'])
                return
            if ttsu.download_clip("_temp",
                                  all_data[1].strip(),
                                  all_data[2].strip(),
                                  directory=f'{dir_utils.get_temp_med_dir()}'
                                  ):
                tts_settings.current_track = "_temp"
                GS.vlc_interface.toggle_repeat(repeat=False)
                GS.vlc_interface.toggle_loop(loop=False)
                GS.vlc_interface.clear_playlist()
                GS.vlc_interface.add_and_play_to_playlist(
                    mrl=f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}/{tts_settings.current_track}.oga')
                ttsu.play_audio()
                return
        GS.gui_service.quick_gui(
            f"Incorrect Format:<br>{get_command_token()}tts 'voice_name' 'message'<br>OR<br>{get_command_token()}tts 'message'",
            text_type='header',
            box_align='left',
            user=data_actor['name'])
