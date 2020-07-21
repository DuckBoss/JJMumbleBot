from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.utility import sound_board_utility as sbu
from JJMumbleBot.plugins.extensions.sound_board.utility import settings as sbu_settings
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.vlc.vlc_api import TrackType, TrackInfo
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
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        sbu_settings.sound_board_metadata = self.metadata
        sbu_settings.plugin_name = self.plugin_name
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        if gs.vlc_interface.check_dni_is_mine(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]):
            gs.vlc_interface.stop()
            gs.audio_dni = None
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}')
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def cmd_sblist(self, data):
        internal_list = []
        data_actor = gs.mumble_inst.users[data.actor]
        gather_list = sbu.prepare_sb_list()
        for i, item in enumerate(gather_list):
            internal_list.append(
                f"<br><font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")
        cur_text = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local Sound Board Files:</font>"
        if len(internal_list) == 0:
            cur_text += "<br>There are no local sound board files available."
            gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left',
                                     user=data_actor['name'])
            log(INFO, "Displayed a list of all local sound board files.")
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
        log(INFO, "Displayed a list of all local sound board files.")

    def cmd_sbdownload(self, data):
        all_data = data.message.strip().split()
        url_stripped = BeautifulSoup(all_data[1], features='html.parser').get_text()
        if len(all_data) > 2:
            if "youtube.com" in url_stripped or "youtu.be" in url_stripped:
                sbu.download_clip(url_stripped, all_data[2].strip())
                gs.gui_service.quick_gui(f"Downloaded sound clip as : {all_data[2].strip()}.wav",
                                         text_type='header',
                                         box_align='left')
                return
            return

    def cmd_sbdelete(self, data):
        all_data = data.message().strip().split()
        if len(all_data) == 2:
            if ".wav" in all_data[1].strip():
                dir_utils.remove_file(all_data[1].strip(), f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/")
                gs.gui_service.quick_gui(f"Deleted sound clip : {all_data[1].strip()}", text_type='header',
                                         box_align='left')

    def cmd_sbrandom(self, data):
        if gs.vlc_interface.check_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]):
            gs.vlc_interface.set_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return
        sender = gs.mumble_inst.users[data.actor]['name']
        gather_list = sbu.prepare_sb_list()
        random.seed(datetime.now())
        random_sfx = random.choice(gather_list)[:-4]
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{random_sfx}.wav',
            name=random_sfx,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=False
        )
        gs.vlc_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False
        )
        gs.vlc_interface.play(override=self.metadata.getboolean(C_PLUGIN_SETTINGS, P_ENABLE_QUEUE, fallback=False))

    def cmd_sb(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return

        if gs.vlc_interface.check_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]):
            gs.vlc_interface.set_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        sender = gs.mumble_inst.users[data.actor]['name']
        to_play = all_data[1].strip()
        if not path.exists(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav"):
            gs.gui_service.quick_gui(
                f"The sound clip '{to_play}.wav' does not exist.",
                text_type='header',
                box_align='left')
            if gs.vlc_interface.get_track().name == '':
                gs.vlc_interface.clear_dni()
            return
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav',
            name=to_play,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=False
        )
        gs.vlc_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False
        )
        gs.vlc_interface.play(override=self.metadata.getboolean(C_PLUGIN_SETTINGS, P_ENABLE_QUEUE, fallback=False))

    def cmd_sbquiet(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return

        if gs.vlc_interface.check_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME], quiet=True):
            gs.vlc_interface.set_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        sender = gs.mumble_inst.users[data.actor]['name']
        to_play = all_data[1].strip()
        if not path.exists(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav"):
            gs.gui_service.quick_gui(
                "The sound clip does not exist.",
                text_type='header',
                box_align='left')
            if gs.vlc_interface.get_track().name == '':
                gs.vlc_interface.clear_dni()
            return
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav',
            name=to_play,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=True
        )
        gs.vlc_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False
        )
        gs.vlc_interface.play(override=self.metadata.getboolean(C_PLUGIN_SETTINGS, P_ENABLE_QUEUE, fallback=False))

    def cmd_sbquietoverride(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return

        if gs.vlc_interface.check_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME], quiet=True):
            gs.vlc_interface.set_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        sender = gs.mumble_inst.users[data.actor]['name']
        to_play = all_data[1].strip()
        if not path.exists(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav"):
            gs.gui_service.quick_gui(
                "The sound clip does not exist.",
                text_type='header',
                box_align='left')
            if gs.vlc_interface.get_track().name == '':
                gs.vlc_interface.clear_dni()
            return
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{to_play}.wav',
            name=to_play,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=True
        )
        gs.vlc_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False
        )
        gs.vlc_interface.play(override=True)
