from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.audio.audio_api import TrackInfo, TrackType, AudioLibrary
from JJMumbleBot.settings import global_settings as gs
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
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        tts_settings.plugin_name = self.plugin_name
        tts_settings.voice_list = loads(self.metadata.get(C_PLUGIN_SETTINGS, P_TTS_ALL_VOICE))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        if gs.aud_interface.check_dni_is_mine(self.plugin_name):
            gs.aud_interface.stop()
            gs.audio_dni = None
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/text_to_speech')
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def cmd_ttsstop(self, data):
        if gs.aud_interface.check_dni_is_mine(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]):
            gs.aud_interface.stop()
            gs.gui_service.quick_gui("Stopped text-to-speech audio.", text_type='header',
                                     box_align='left')

    def cmd_ttslist(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        internal_list = []
        gather_list = ttsu.prepare_tts_list()
        for i, item in enumerate(gather_list):
            internal_list.append(
                f"<br><font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")
        cur_text = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local TTS Files:</font>"
        if len(internal_list) == 0:
            cur_text += "<br>There are no local text to speech files available."
            gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left',
                                     user=data_actor['name'])
            log(INFO, "Displayed a list of all local text to speech files.", origin=L_COMMAND)
            return
        for i, item in enumerate(internal_list):
            cur_text += item
            if i % 50 == 0 and i != 0:
                gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                         user=data_actor['name'])
                cur_text = ""
        if cur_text != "":
            gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                     user=data_actor['name'])
        log(INFO, "Displayed a list of all local text to speech files.", origin=L_COMMAND)

    def cmd_ttsvoices(self, data):
        if len(tts_settings.voice_list) == 0:
            cur_text = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Available Voices:</font> None"
            gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left')
            log(INFO, "Displayed a list of all available text to speech voices.", origin=L_COMMAND)
            return
        cur_text = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Available Voices:</font>"
        for i, voice_name in enumerate(tts_settings.voice_list):
            cur_text += f"[{i}] - {voice_name}<br>"
        gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left')
        log(INFO, "Displayed a list of all available text to speech voices.", origin=L_COMMAND)

    def cmd_ttsdownload(self, data):
        all_data = data.message.strip().split(' ', 3)
        if ttsu.download_clip(all_data[1].strip(), all_data[2].strip(), all_data[3].strip()):
            gs.gui_service.quick_gui(f"Downloaded text-to-speech clip as : {all_data[1].strip()}",
                                     text_type='header',
                                     box_align='left')
            return

    def cmd_ttsdelete(self, data):
        all_data = data.message.strip().split(' ', 1)
        if ".wav" in all_data[1].strip():
            dir_utils.remove_file(all_data[1].strip(), f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/")
            gs.gui_service.quick_gui(f"Deleted text-to-speech clip : {all_data[1].strip()}",
                                     text_type='header',
                                     box_align='left')
            return
        return

    def cmd_ttsplay(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return
        all_data = data.message.strip().split(' ', 1)
        to_play = all_data[1].strip()
        if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.oga"):
            gs.gui_service.quick_gui(
                f"The text-to-speech clip '{to_play}.oga' does not exist.",
                text_type='header',
                box_align='left')
            if gs.aud_interface.get_track().name == '':
                gs.aud_interface.clear_dni()
            return
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.oga',
            name=to_play,
            sender=gs.mumble_inst.users[data.actor]['name'],
            duration=None,
            track_type=TrackType.FILE,
            quiet=False
        )
        gs.aud_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False
        )
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG, override=True)

    def cmd_ttsplayquiet(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return
        all_data = data.message.strip().split(' ', 1)
        to_play = all_data[1].strip()
        if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.oga"):
            gs.gui_service.quick_gui(
                f"The text-to-speech clip '{to_play}.oga' does not exist.",
                text_type='header',
                box_align='left')
            if gs.aud_interface.get_track().name == '':
                gs.aud_interface.clear_dni()
            return
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.oga',
            name=to_play,
            sender=gs.mumble_inst.users[data.actor]['name'],
            duration=None,
            track_type=TrackType.FILE,
            quiet=True
        )
        gs.aud_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False,
            quiet=True
        )
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG, override=True)

    def cmd_tts(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return
        data_actor = gs.mumble_inst.users[data.actor]
        all_data = data.message.strip().split(' ', 2)

        if all_data[1].strip() in tts_settings.voice_list:
            all_data = data.message.strip().split(' ', 2)
        else:
            all_data = data.message.strip().split(' ', 1)

        if len(all_data) == 2:
            if len(all_data[1]) > int(self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]):
                gs.gui_service.quick_gui(
                    f"The text-to-speech message exceeded the character limit:"
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
                track_obj = TrackInfo(
                    uri=f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}/_temp.oga',
                    name='text-to-speech clip',
                    sender=gs.mumble_inst.users[data.actor]['name'],
                    duration=None,
                    track_type=TrackType.FILE,
                    quiet=True
                )
                gs.aud_interface.enqueue_track(
                    track_obj=track_obj,
                    to_front=False,
                    quiet=True
                )
                gs.aud_interface.play(audio_lib=AudioLibrary.VLC, override=True)
        elif len(all_data) == 3:
            if len(all_data[1]) > int(self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]):
                gs.gui_service.quick_gui(
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
                track_obj = TrackInfo(
                    uri=f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}/_temp.oga',
                    name='text-to-speech clip',
                    sender=gs.mumble_inst.users[data.actor]['name'],
                    duration=None,
                    track_type=TrackType.FILE,
                    quiet=True
                )
                gs.aud_interface.enqueue_track(
                    track_obj=track_obj,
                    to_front=False,
                    quiet=True
                )
                gs.aud_interface.play(audio_lib=AudioLibrary.VLC, override=True)
        else:
            gs.gui_service.quick_gui(
                f"Incorrect Format:<br>{get_command_token()}tts 'voice_name' 'message'<br>OR<br>{get_command_token()}tts 'message'",
                text_type='header',
                box_align='left',
                user=data_actor['name'])
