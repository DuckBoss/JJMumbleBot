from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.utility import sound_board_utility as sbu
from JJMumbleBot.lib.utils import dir_utils
import os
import random
from datetime import datetime
from bs4 import BeautifulSoup


class Plugin(PluginBase):
    def quit(self):
        sbu.clear_audio_thread()
        sbu.stop_audio()
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/sound_board')
        sbu.exit_flag = True
        dprint("Exiting Sound Board Plugin...")

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
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_DIR][P_PERM_MEDIA_DIR]}/sound_board/')
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_DIR][P_TEMP_MED_DIR]}/sound_board/')
        sbu.sound_board_metadata = self.metadata
        sbu.volume = float(self.metadata[C_PLUGIN_SETTINGS][P_DEF_VOL])
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "sbstop":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if sbu.is_playing and GS.audio_inst is not None:
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
                sbu.stop_audio()
                GS.gui_service.quick_gui("Stopping sound board audio thread...", text_type='header', box_align='left')
                return
            return

        elif command == "sbvolume":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                GS.gui_service.quick_gui(f"Current sound board volume: {sbu.volume}", text_type='header',
                                         box_align='left')
                return
            if vol > 1 or vol < 0:
                GS.gui_service.quick_gui("Invalid sound_board volume Input: [0-1]", text_type='header',
                                         box_align='left')
                return
            sbu.volume = vol
            GS.gui_service.quick_gui(f"Set sound_board volume to {sbu.volume}", text_type='header',
                                     box_align='left')
            return

        elif command == "sblist":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
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
                GS.log_service.info("Displayed a list of all local sound board files.")
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
            GS.log_service.info("Displayed a list of all local sound board files.")
            return

        elif command == "sblist_echo":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
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
                GS.log_service.info("Displayed a list of all local sound board files.")
                return
            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
                    cur_text = ""
            if cur_text != "":
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
            GS.log_service.info("Displayed a list of all local sound board files.")
            return

        elif command == "sbdownload":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
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
            return

        elif command == "sbdelete":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            all_messages = message[1:].split()
            if len(all_messages) == 2:
                if ".wav" in all_messages[1].strip():
                    dir_utils.remove_file(all_messages[1].strip(), dir_utils.get_perm_med_dir() + "sound_board/")
                    GS.gui_service.quick_gui(f"Deleted sound clip : {all_messages[1].strip()}", text_type='header',
                                             box_align='left')

        elif command == "sbrandom":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if not GS.audio_dni[0]:
                GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
            else:
                if GS.audio_dni-[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
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
            sfx_duration = sbu.get_audio_length(random_sfx)
            while sfx_duration > 6:
                random_sfx = random.choice(gather_list)[:-4]
                sfx_duration = sbu.get_audio_length(random_sfx)

            # print(random_sfx)
            if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/sound_board/{random_sfx}.wav"):
                GS.gui_service.quick_gui(
                    "The sound clip does not exist.",
                    text_type='header',
                    box_align='left')
                return False
            sbu.current_track = random_sfx
            sbu.play_audio()

        elif command == "sb":
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
            # print(GS.audio_dni)
            parameter = message_parse[1].strip()
            if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/sound_board/{parameter}.wav"):
                GS.gui_service.quick_gui(
                    "The sound clip does not exist.",
                    text_type='header',
                    box_align='left')
                return False
            sbu.current_track = parameter
            sbu.play_audio()
