from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.resources.strings import *
from JJMumbleBot.plugins.extensions.sound_board.utility import sound_board_utility as sbu
from JJMumbleBot.plugins.extensions.sound_board.utility import settings as sbu_settings
from JJMumbleBot.lib.utils.runtime_utils import get_command_token
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.audio.audio_api import TrackType, TrackInfo, AudioLibrary
from os import path
import random
from datetime import datetime
from bs4 import BeautifulSoup


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.is_running = True
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        sbu_settings.sound_board_metadata = self.metadata
        sbu_settings.plugin_name = self.plugin_name
        log(
            INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value
        )

    def quit(self):
        if gs.aud_interface.check_dni_is_mine(self.plugin_name):
            gs.aud_interface.stop()
            gs.audio_dni = None
        self.is_running = False
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}')
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN, print_mode=PrintMode.REG_PRINT.value)

    def stop(self):
        if self.is_running:
            self.quit()

    def start(self):
        if not self.is_running:
            self.__init__()

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
        data_stripped = BeautifulSoup(data.message.strip(), features='html.parser').get_text()
        all_data = data_stripped.split()

        if len(all_data) >= 3:
            if "youtube.com" in data_stripped or "youtu.be" in data_stripped:
                if sbu.find_file(all_data[2].strip()):
                    gs.gui_service.quick_gui(
                        f"A sound clip with the name {all_data[2].strip()} already exists!",
                        text_type='header',
                        box_align='left')
                    return
                if len(all_data) == 4:
                    time_range = all_data[3].strip().split('-')
                    if time_range:
                        sbu.download_clip(all_data[1], all_data[2].strip(),
                                          time_range=time_range,
                                          ffmpeg_path=gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_FFMPEG_PATH],
                                          proxy=gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_PROXY_URL])
                        gs.gui_service.quick_gui(f"Downloaded sound clip as : {all_data[2].strip()}[{time_range[0]}-{time_range[1]}]",
                                                 text_type='header',
                                                 box_align='left')
                    else:
                        gs.gui_service.quick_gui(
                            f"Incorrect Formatting! Format: {get_command_token()}sbdownload 'youtube_link' 'file_name' 'XXh:XXm:XXs-XXh:XXm:XXs",
                            text_type='header',
                            box_align='left')
                else:
                    if "youtube.com" in data_stripped or "youtu.be" in all_data[1]:
                        sbu.download_clip(all_data[1], all_data[2].strip(),
                                          ffmpeg_path=gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_FFMPEG_PATH],
                                          proxy=gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_PROXY_URL])
                        gs.gui_service.quick_gui(f"Downloaded sound clip as : {all_data[2].strip()}",
                                                 text_type='header',
                                                 box_align='left')
                    else:
                        gs.gui_service.quick_gui(
                            f"Incorrect Formatting! Format: {get_command_token()}sbdownload 'youtube_link' 'file_name' 'XXh:XXm:XXs-XXh:XXm:XXs",
                            text_type='header',
                            box_align='left')
            else:
                gs.gui_service.quick_gui(
                    f"The given link was not identified as a youtube link!",
                    text_type='header',
                    box_align='left')
        else:
            gs.gui_service.quick_gui(
                f"Incorrect Formatting! Format: {get_command_token()}sbdownload 'youtube_link' 'file_name' 'XXh:XXm:XXs-XXh:XXm:XXs'(optional)",
                text_type='header',
                box_align='left')

    def cmd_sbdelete(self, data):
        all_data = data.message.strip().split()
        if len(all_data) == 2:
            audio_clip = sbu.find_file(all_data[1].strip())
            if audio_clip:
                dir_utils.remove_file(audio_clip, f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/")
                gs.gui_service.quick_gui(f"Deleted sound clip : {audio_clip}", text_type='header',
                                         box_align='left')

    def cmd_sbrandom(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return
        sender = gs.mumble_inst.users[data.actor]['name']
        gather_list = sbu.prepare_sb_list(include_file_extensions=True)
        random.seed(datetime.now())
        random_sfx = random.choice(gather_list)
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{random_sfx}',
            name=random_sfx,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=False
        )
        gs.aud_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False
        )
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG,
                              override=self.metadata.getboolean(C_PLUGIN_SETTINGS, P_ENABLE_QUEUE, fallback=False))

    def cmd_sbrandomquiet(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return
        sender = gs.mumble_inst.users[data.actor]['name']
        gather_list = sbu.prepare_sb_list(include_file_extensions=True)
        random.seed(datetime.now())
        random_sfx = random.choice(gather_list)
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{random_sfx}',
            name=random_sfx,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=True
        )
        gs.aud_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False,
            quiet=True
        )
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG,
                              override=self.metadata.getboolean(C_PLUGIN_SETTINGS, P_ENABLE_QUEUE, fallback=False))

    def cmd_sbrandomnow(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return
        sender = gs.mumble_inst.users[data.actor]['name']
        gather_list = sbu.prepare_sb_list(include_file_extensions=True)
        random.seed(datetime.now())
        random_sfx = random.choice(gather_list)
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{random_sfx}',
            name=random_sfx,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=False
        )
        gs.aud_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False,
            quiet=True
        )
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG, override=True)

    def cmd_sbrandomquietnow(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return
        sender = gs.mumble_inst.users[data.actor]['name']
        gather_list = sbu.prepare_sb_list(include_file_extensions=True)
        random.seed(datetime.now())
        random_sfx = random.choice(gather_list)
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{random_sfx}',
            name=random_sfx,
            sender=sender,
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

    def cmd_sbsearch(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            return
        search_query = all_data[1].strip()
        audio_clips = sbu.find_files(search_query)
        match_str = f"Search Results for <font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{search_query}</font>: "
        if len(audio_clips) > 0:
            for i, clip in enumerate(audio_clips):
                match_str += f"<br><font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{i+1}]</font> - {clip}"
        else:
            match_str += "None"
        gs.gui_service.quick_gui(
            match_str,
            text_type='header',
            text_align='left',
            box_align='left'
        )

    def cmd_sb(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return

        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        sender = gs.mumble_inst.users[data.actor]['name']
        to_play = all_data[1].strip()
        audio_clip = sbu.find_file(to_play)
        if not audio_clip:
            gs.gui_service.quick_gui(
                f"The sound clip '{to_play}' does not exist.",
                text_type='header',
                box_align='left'
            )
            gs.aud_interface.clear_dni()
            return
        # print(f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}')
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
            alt_uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
            name=to_play,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=False
        )
        gs.aud_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False,
        )
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG,
                              override=self.metadata.getboolean(C_PLUGIN_SETTINGS, P_ENABLE_QUEUE, fallback=False))

    def cmd_sbnow(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return

        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        sender = gs.mumble_inst.users[data.actor]['name']
        to_play = all_data[1].strip()
        audio_clip = sbu.find_file(to_play)
        if not audio_clip:
            gs.gui_service.quick_gui(
                f"The sound clip '{to_play}' does not exist.",
                text_type='header',
                box_align='left'
            )
            gs.aud_interface.clear_dni()
            return
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
            alt_uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
            name=to_play,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=False
        )
        gs.aud_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False,
            quiet=True
        )
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG, override=True)

    def cmd_sbquiet(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return

        if gs.aud_interface.check_dni(self.plugin_name, quiet=True):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        sender = gs.mumble_inst.users[data.actor]['name']
        to_play = all_data[1].strip()
        audio_clip = sbu.find_file(to_play)
        if not audio_clip:
            gs.gui_service.quick_gui(
                f"The sound clip '{to_play}' does not exist.",
                text_type='header',
                box_align='left'
            )
            gs.aud_interface.clear_dni()
            return
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
            alt_uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
            name=to_play,
            sender=sender,
            duration=None,
            track_type=TrackType.FILE,
            quiet=True
        )
        gs.aud_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False,
            quiet=True
        )
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG,
                              override=self.metadata.getboolean(C_PLUGIN_SETTINGS, P_ENABLE_QUEUE, fallback=False))

    def cmd_sbquietnow(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return

        if gs.aud_interface.check_dni(self.plugin_name, quiet=True):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        sender = gs.mumble_inst.users[data.actor]['name']
        to_play = all_data[1].strip()
        audio_clip = sbu.find_file(to_play)
        if not path.exists(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}"):
            gs.gui_service.quick_gui(
                f"The sound clip '{to_play}' does not exist.",
                text_type='header',
                box_align='left'
            )
            gs.aud_interface.clear_dni()
            return
        track_obj = TrackInfo(
            uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
            alt_uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
            name=to_play,
            sender=sender,
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
