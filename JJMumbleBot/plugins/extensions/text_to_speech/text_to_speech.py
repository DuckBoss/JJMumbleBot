from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.text_to_speech.utility import text_to_speech_utility as ttsu
from JJMumbleBot.plugins.extensions.text_to_speech.resources.strings import *
from JJMumbleBot.lib.utils import dir_utils
import os


class Plugin(PluginBase):
    def quit(self):
        ttsu.clear_audio_thread()
        ttsu.stop_audio()
        ttsu.exit_flag = True
        dprint("Exiting Text To Speech Plugin...")

    def get_metadata(self):
        pass

    def __init__(self):
        super().__init__()
        import json
        raw_file = os.path.basename(__file__)
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{raw_file}')
        self.plugin_cmds = json.loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.priv_path = f'plugins/extensions/{raw_file.split(".")[0]}/privileges.csv'
        self.help_path = f'plugins/extensions/{raw_file.split(".")[0]}/help.html'
        ttsu.tts_metadata = self.metadata
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "ttsstop":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if ttsu.is_playing and GS.audio_inst is not None:
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
            return

        if command == "ttsv":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                GS.gui_service.quick_gui(f"Current text to speech volume: {ttsu.volume}", text_type='header',
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
            ttsu.volume = vol
            GS.gui_service.quick_gui(f"Set text to speech volume to {ttsu.volume}", text_type='header',
                                     box_align='left')
            return

        elif command == "ttslist":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
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
            GS.log_service.info("Displayed a list of all local text to speech files.")
            return

        elif command == "ttslist_echo":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
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
                GS.log_service.info("Displayed a list of all local text to speech files.")
                return
            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
                    cur_text = ""
            if cur_text != "":
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
            GS.log_service.info("Displayed a list of all text to speech board files.")
            return

        elif command == "ttsdownload":
            from JJMumbleBot.plugins.extensions.text_to_speech.resources.strings import P_VLC_DIR

            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            all_messages = message[1:].split(' ', 3)
            if ttsu.download_clip(all_messages[1].strip(), all_messages[2].strip(), all_messages[3].strip()):
                GS.gui_service.quick_gui(f"Downloaded text to speech clip as : {all_messages[1].strip()}.oga",
                                         text_type='header',
                                         box_align='left')
                return
            return

        elif command == "ttsdelete":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
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
            return

        elif command == "ttsplay":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
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
            ttsu.current_track = parameter
            ttsu.play_audio()
            return

        elif command == "ttsplayquiet":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if not GS.audio_dni[0]:
                GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
            else:
                if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                    return
            parameter = message_parse[1].strip()
            if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/text_to_speech/{parameter}.oga"):
                return False
            ttsu.current_track = parameter
            ttsu.play_audio()
            return

        elif command == "tts":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
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
            if len(all_messages) == 2:
                if len(all_messages[1]) > int(self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]):
                    GS.gui_service.quick_gui(
                        f"The text to speech message exceeded the character limit: [{self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]}].",
                        text_type='header',
                        box_align='left',
                        user=GS.mumble_inst.users[text.actor]['name'])
                    return
                if ttsu.download_clip("_temp", self.metadata[C_PLUGIN_SETTINGS][P_TTS_DEF_VOICE], all_messages[1].strip()):
                    ttsu.current_track = "_temp"
                    ttsu.play_audio()
                    return
            elif len(all_messages) == 3:
                if len(all_messages[1]) > int(self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]):
                    GS.gui_service.quick_gui(
                        f"The text to speech message exceeded the character limit: [{self.metadata[C_PLUGIN_SETTINGS][P_TTS_MSG_CHR_LIM]}].",
                        text_type='header',
                        box_align='left',
                        user=GS.mumble_inst.users[text.actor]['name'])
                    return
                if ttsu.download_clip("_temp", all_messages[1].strip(), all_messages[2].strip()):
                    ttsu.current_track = "_temp"
                    ttsu.play_audio()
                    return
            GS.gui_service.quick_gui(
                f"Incorrect Format:<br>!tts 'voice_name' 'message'<br>OR<br>!tts 'message'",
                text_type='header',
                box_align='left',
                user=GS.mumble_inst.users[text.actor]['name'])
            return
