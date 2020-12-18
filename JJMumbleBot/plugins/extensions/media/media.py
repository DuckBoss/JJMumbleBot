from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.audio.audio_api import TrackInfo, TrackType, AudioLibrary
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.media.resources.strings import *
from JJMumbleBot.plugins.extensions.media.utility import media_utility as md_utility
from JJMumbleBot.plugins.extensions.media.utility import settings as md_settings
from JJMumbleBot.lib.utils.runtime_utils import get_command_token
import warnings
import os
import requests
from datetime import timedelta
from bs4 import BeautifulSoup


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}')
        warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
        md_settings.youtube_metadata = self.metadata
        md_settings.plugin_name = self.plugin_name
        self.register_callbacks()
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
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}')
        log(
            INFO,
            f"Exiting {self.plugin_name} plugin...",
            origin=L_SHUTDOWN,
            print_mode=PrintMode.REG_PRINT.value
        )

    def register_callbacks(self):
        for method_name in dir(md_utility):
            if callable(getattr(md_utility, method_name)) and not method_name[0].isupper() \
                    and not method_name[0] == '_' \
                    and not method_name == 'register_callbacks'\
                    and not method_name[:3] == 'cmd'\
                    and not method_name == 'quit':
                gs.plugin_callbacks.register_callback(
                    f'{self.plugin_name}|{method_name}|clbk',
                    getattr(md_utility, method_name)
                )
                log(INFO, f"Registered audio interface callback {self.plugin_name}|{method_name}|clbk",
                    origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_ytplaylist(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            gs.gui_service.quick_gui(
                f"Invalid formatting! Format: {get_command_token()}ytplaylist 'youtube_playlist_link'",
                text_type='header',
                box_align='left')
            gs.aud_interface.clear_dni()
            return
        sender = gs.mumble_inst.users[data.actor]['name']
        stripped_url = BeautifulSoup(all_data[1], features='html.parser').get_text()

        check_url_request = requests.get(f'https://www.youtube.com/oembed?format=json&url={stripped_url}')
        if check_url_request.status_code == 200 and check_url_request.content != "Not Found":
            if "list" in check_url_request.json()['html']:
                all_song_data = md_utility.get_playlist_info(stripped_url)
                if all_song_data is None:
                    gs.gui_service.quick_gui(
                        "The youtube playlist information could not be retrieved.",
                        text_type='header',
                        box_align='left')
                    gs.aud_interface.clear_dni()
                    return

                for i, song_data in enumerate(all_song_data):
                    track_obj = TrackInfo(
                        uri=song_data['main_url'],
                        name=song_data['main_title'],
                        sender=sender,
                        duration=-1,
                        track_type=TrackType.STREAM,
                        track_id=song_data['main_id'],
                        alt_uri=song_data['std_url'],
                        image_uri=f"{dir_utils.get_temp_med_dir()}/{self.plugin_name}/{song_data['main_id']}",
                        quiet=False
                    )
                    gs.aud_interface.enqueue_track(
                        track_obj=track_obj,
                        to_front=False,
                        quiet=True
                    )
                gs.gui_service.quick_gui(
                    "The playlist was generated and added to the audio queue.",
                    text_type='header',
                    box_align='left')
                gs.aud_interface.play(audio_lib=AudioLibrary.VLC)
            else:
                gs.aud_interface.clear_dni()
                gs.gui_service.quick_gui(
                    "The given link was not a playlist.<br>Only use the !ytplaylist command for playlist links.",
                    text_type='header',
                    box_align='left')
        else:
            gs.aud_interface.clear_dni()
            gs.gui_service.quick_gui(
                "The given link was not identified as a Youtube playlist link!<br>SoundCloud playlists are not supported.",
                text_type='header',
                box_align='left')

    def cmd_link(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_LINK, origin=L_COMMAND,
                error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                CMD_INVALID_LINK,
                text_type='header',
                box_align='left')
            gs.aud_interface.clear_dni()
            return
        sender = gs.mumble_inst.users[data.actor]['name']
        stripped_url = BeautifulSoup(all_data[1], features='html.parser').get_text()
        if "youtube.com" in stripped_url or "youtu.be" in stripped_url or 'soundcloud' in stripped_url:
            if ("youtube.com" in stripped_url and "list" in stripped_url) or ("soundcloud" in stripped_url and "sets" in stripped_url):
                gs.gui_service.quick_gui(
                    "The given link was identified as a playlist link!<br>Please use the playlist "
                    "command to add playlists to the queue!",
                    text_type='header',
                    box_align='left')
                gs.aud_interface.clear_dni()
                return

            song_data = md_utility.get_video_info(stripped_url)
            if song_data is None:
                gs.gui_service.quick_gui(
                    "The media track information could not be retrieved.",
                    text_type='header',
                    box_align='left')
                gs.aud_interface.clear_dni()
                return
            if int(song_data['duration']) > int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_VID_LEN]):
                gs.gui_service.quick_gui(
                    f"The media track provided is longer than the maximum allowed video duration: [{str(timedelta(seconds=int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_VID_LEN])))}]",
                    text_type='header',
                    box_align='left')
                gs.aud_interface.clear_dni()
                return
            track_obj = TrackInfo(
                uri=song_data['main_url'],
                name=song_data['main_title'],
                sender=sender,
                duration=str(timedelta(seconds=int(song_data['duration']))) if int(song_data['duration']) > 0 else -1,
                track_type=TrackType.STREAM,
                track_id=song_data['main_id'],
                alt_uri=stripped_url,
                image_uri=f"{dir_utils.get_temp_med_dir()}/{self.plugin_name}/{song_data['main_id']}",
                quiet=False
            )
            gs.aud_interface.enqueue_track(
                track_obj=track_obj,
                to_front=False
            )
            gs.aud_interface.play(audio_lib=AudioLibrary.VLC)

    def cmd_linkfront(self, data):
        if gs.aud_interface.check_dni(self.plugin_name):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_LINK_FRONT, origin=L_COMMAND,
                error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                CMD_INVALID_LINK_FRONT,
                text_type='header',
                box_align='left')
            gs.aud_interface.clear_dni()
            return
        sender = gs.mumble_inst.users[data.actor]['name']
        stripped_url = BeautifulSoup(all_data[1], features='html.parser').get_text()
        if "youtube.com" in stripped_url or "youtu.be" in stripped_url or 'soundcloud' in stripped_url:
            if ("youtube.com" in stripped_url and "list" in stripped_url) or (
                    "soundcloud" in stripped_url and "sets" in stripped_url):
                gs.gui_service.quick_gui(
                    "The given link was identified as a playlist link!<br>Please use the playlist "
                    "command to add playlists to the queue!",
                    text_type='header',
                    box_align='left')
                gs.aud_interface.clear_dni()
                return

            song_data = md_utility.get_video_info(stripped_url)
            if song_data is None:
                gs.gui_service.quick_gui(
                    "The media track information could not be retrieved.",
                    text_type='header',
                    box_align='left')
                gs.aud_interface.clear_dni()
                return
            if int(song_data['duration']) > int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_VID_LEN]):
                gs.gui_service.quick_gui(
                    f"The media track provided is longer than the maximum allowed video duration: [{str(timedelta(seconds=int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_VID_LEN])))}]",
                    text_type='header',
                    box_align='left')
                gs.aud_interface.clear_dni()
                return
            track_obj = TrackInfo(
                uri=song_data['main_url'],
                name=song_data['main_title'],
                sender=sender,
                duration=str(timedelta(seconds=int(song_data['duration']))) if int(song_data['duration']) > 0 else -1,
                track_type=TrackType.STREAM,
                track_id=song_data['main_id'],
                alt_uri=stripped_url,
                image_uri=f"{dir_utils.get_temp_med_dir()}/{self.plugin_name}/{song_data['main_id']}",
                quiet=False
            )
            gs.aud_interface.enqueue_track(
                track_obj=track_obj,
                to_front=True
            )
            gs.aud_interface.play(audio_lib=AudioLibrary.VLC)

    def cmd_ytsearch(self, data):
        all_data = data.message.strip().split(' ', 1)
        try:
            search_term = all_data[1]
        except IndexError:
            log(ERROR, CMD_INVALID_YTSEARCH, origin=L_COMMAND,
                error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                CMD_INVALID_YTSEARCH,
                text_type='header',
                box_align='left')
            return
        search_results = md_utility.get_search_results(search_term, int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_SEARCH_LEN]))
        log(INFO, "Displayed youtube search results.", origin=L_COMMAND)
        gs.gui_service.quick_gui(
            search_results,
            text_type='header',
            text_align='left',
            box_align='left')
        md_settings.can_play = True

    def cmd_ytplay(self, data):
        if not gs.aud_interface.check_dni_active() or gs.aud_interface.check_dni_is_mine(self.plugin_name):
            all_data = data.message.strip().split()
            sender = gs.mumble_inst.users[data.actor]['name']
            if len(all_data) == 1:
                song_data = md_utility.get_video_info(f"https://www.youtube.com{md_settings.search_results[0]['href']}")
                if song_data is None:
                    gs.gui_service.quick_gui(
                        f"There was an error with the chosen video.",
                        text_type='header',
                        box_align='left')
                    return
                gs.gui_service.quick_gui(
                    f"Automatically chosen: {md_settings.search_results[0]['title']}",
                    text_type='header',
                    box_align='left')
                md_settings.can_play = False
                gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
                track_obj = TrackInfo(
                    uri=song_data['main_url'],
                    name=song_data['main_title'],
                    sender=sender,
                    duration=str(timedelta(seconds=int(song_data['duration']))) if int(
                        song_data['duration']) > 0 else -1,
                    track_type=TrackType.STREAM,
                    track_id=song_data['main_id'],
                    alt_uri=f"https://www.youtube.com{md_settings.search_results[0]['href']}",
                    image_uri=f"{dir_utils.get_temp_med_dir()}/{self.plugin_name}/{song_data['main_id']}",
                    quiet=False
                )
                gs.aud_interface.enqueue_track(
                    track_obj=track_obj,
                    to_front=False
                )
                md_settings.search_results = None
                gs.aud_interface.play(audio_lib=AudioLibrary.VLC)
            elif len(all_data) == 2:
                if int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_SEARCH_LEN]) >= int(all_data[1]) >= 0:
                    song_data = md_utility.get_video_info(f"https://www.youtube.com{md_settings.search_results[int(all_data[1])]['href']}")
                    if song_data is None:
                        gs.gui_service.quick_gui(
                            f"There was an error with the chosen video.",
                            text_type='header',
                            box_align='left')
                        return
                    gs.gui_service.quick_gui(
                        f"You've chosen: {md_settings.search_results[int(all_data[1])]['title']}",
                        text_type='header',
                        box_align='left')
                    md_settings.can_play = False
                else:
                    gs.gui_service.quick_gui(
                        f"Invalid choice! Valid Range [0-{int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_SEARCH_LEN])}]",
                        text_type='header',
                        box_align='left')
                    md_settings.can_play = False
                    return
                gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
                track_obj = TrackInfo(
                    uri=song_data['main_url'],
                    name=song_data['main_title'],
                    sender=sender,
                    duration=str(timedelta(seconds=int(song_data['duration']))) if int(
                        song_data['duration']) > 0 else -1,
                    track_type=TrackType.STREAM,
                    track_id=song_data['main_id'],
                    alt_uri=f"https://www.youtube.com{md_settings.search_results[int(all_data[1])]['href']}",
                    image_uri=f"{dir_utils.get_temp_med_dir()}/{self.plugin_name}/{song_data['main_id']}",
                    quiet=False
                )
                gs.aud_interface.enqueue_track(
                    track_obj=track_obj,
                    to_front=False
                )
                md_settings.search_results = None
                gs.aud_interface.play(audio_lib=AudioLibrary.VLC)
            else:
                md_settings.can_play = False
                md_settings.search_results = None
                log(ERROR, CMD_INVALID_YTPLAY, origin=L_COMMAND,
                    error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
                gs.gui_service.quick_gui(
                    CMD_INVALID_YTPLAY,
                    text_type='header',
                    box_align='left')
