from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib import privileges
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
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_DIR][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_DIR][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        tts_settings.tts_metadata = self.metadata
        tts_settings.voice_list = loads(self.metadata.get(C_PLUGIN_SETTINGS, P_TTS_ALL_VOICE))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        ttsu.clear_audio_thread()
        ttsu.stop_audio()
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/text_to_speech')
        tts_settings.exit_flag = True
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def get_metadata(self):
        return self.metadata

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "ttsstop":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if tts_settings.is_playing and GS.audio_inst is not None:
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
                ttsu.stop_audio()
                GS.gui_service.quick_gui("Stopping text to speech audio thread...", text_type='header',
                                         box_align='left')
                return

        elif command == "ttsv":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                GS.gui_service.quick_gui(f"Current text to speech volume: {tts_settings.volume}", text_type='header',
                                         box_align='left')
                return
            if vol > 1:
                GS.gui_service.quick_gui("Invalid text to speech volume Input: [0-1]", text_type='header',
                                         box_align='left')
                return
            if vol < 0:
                GS.gui_service.quick_gui("Invalid text to speech volume Input: [0-1]", text_type='header',
                                         box_align='left')
                return
            tts_settings.volume = vol
            GS.gui_service.quick_gui(f"Set text to speech volume to {tts_settings.volume}", text_type='header',
                                     box_align='left')

        elif command == "ttslist":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            internal_list = []
            gather_list = ttsu.prepare_tts_list()
            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")
            cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local TTS Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local text to speech files available."
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left',
                                         user=GS.mumble_inst.users[text.actor]['name'])
                GS.log_service.info("Displayed a list of all local text to speech files.")
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
            log(INFO, "Displayed a list of all local text to speech files.", origin=L_COMMAND)

        elif command == "ttslist_echo":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            internal_list = []
            gather_list = ttsu.prepare_tts_list()

            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")
            cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local TTS Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local text to speech files available."
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left')
                log(INFO, "Displayed a list of all local text to speech files.", origin=L_COMMAND)
                return
            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
                    cur_text = ""
            if cur_text != "":
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
            log(INFO, "Displayed a list of all text to speech board files.", origin=L_COMMAND)

        elif command == "ttsvoices":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
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

        elif command == "ttsdownload":
            from JJMumbleBot.plugins.extensions.text_to_speech.resources.strings import P_VLC_DIR

            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            all_messages = message[1:].split(' ', 3)
            if ttsu.download_clip(all_messages[1].strip(), all_messages[2].strip(), all_messages[3].strip()):
                GS.gui_service.quick_gui(f"Downloaded text to speech clip as : {all_messages[1].strip()}.oga",
                                         text_type='header',
                                         box_align='left')
                return

        elif command == "ttsdelete":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            all_messages = message[1:].split()
            if len(all_messages) == 2:
                if ".oga" in all_messages[1].strip():
                    dir_utils.remove_file(all_messages[1].strip(), f"{dir_utils.get_perm_med_dir()}/text_to_speech/")
                    GS.gui_service.quick_gui(f"Deleted text to speech clip : {all_messages[1].strip()}",
                                             text_type='header',
                                             box_align='left')
                    return
                return

        elif command == "ttsplay":
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
            parameter = message_parse[1].strip()
            if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/text_to_speech/{parameter}.oga"):
                GS.gui_service.quick_gui(
                    "The text to speech clip does not exist.",
                    text_type='header',
                    box_align='left')
                return False
            tts_settings.current_track = parameter
            ttsu.play_audio()

        elif command == "ttsplayquiet":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if not GS.audio_dni[0]:
                GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
            else:
                if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                    return
            parameter = message_parse[1].strip()
            if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/text_to_speech/{parameter}.oga"):
                return False
            tts_settings.current_track = parameter
            ttsu.play_audio()

        elif command == "tts":
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
            all_messages = message[1:].split(' ', 2)
            if all_messages[1].strip() in tts_settings.voice_list:
                all_messages = message[1:].split(' ', 2)
            else:
                all_messages = message[1:].split(' ', 1)

            if len(all_messages) == 2:
                if len(all_messages[1]) > int(self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]):
                    GS.gui_service.quick_gui(
                        f"The text to speech message exceeded the character limit:"
                        f" [{self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]}].",
                        text_type='header',
                        box_align='left',
                        user=GS.mumble_inst.users[text.actor]['name'])
                    return
                if ttsu.download_clip("_temp",
                                      self.metadata[C_PLUGIN_SETTINGS][P_TTS_DEF_VOICE],
                                      all_messages[1].strip(),
                                      directory=f'{dir_utils.get_temp_med_dir()}'
                                      ):
                    tts_settings.current_track = "_temp"
                    ttsu.play_audio(mode=0)
                    return
            elif len(all_messages) == 3:
                if len(all_messages[1]) > int(self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]):
                    GS.gui_service.quick_gui(
                        f"The text to speech message exceeded the character limit:"
                        f" [{self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]}].",
                        text_type='header',
                        box_align='left',
                        user=GS.mumble_inst.users[text.actor]['name'])
                    return
                if ttsu.download_clip("_temp",
                                      all_messages[1].strip(),
                                      all_messages[2].strip(),
                                      directory=f'{dir_utils.get_temp_med_dir()}'
                                      ):
                    tts_settings.current_track = "_temp"
                    ttsu.play_audio(mode=0)
                    return
            GS.gui_service.quick_gui(
                f"Incorrect Format:<br>!tts 'voice_name' 'message'<br>OR<br>!tts 'message'",
                text_type='header',
                box_align='left',
                user=GS.mumble_inst.users[text.actor]['name'])
