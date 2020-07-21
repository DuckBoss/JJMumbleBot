from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.vlc.vlc_api import TrackInfo, TrackType
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.youtube.utility import youtube_utility as yt_utility
from JJMumbleBot.plugins.extensions.youtube.utility import settings as yt_settings
import warnings
import os
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
        yt_settings.youtube_metadata = self.metadata
        yt_settings.plugin_name = self.plugin_name
        self.register_callbacks()
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        if gs.vlc_interface.check_dni_is_mine(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]):
            gs.vlc_interface.stop()
            gs.audio_dni = None
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}')
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def register_callbacks(self):
        for method_name in dir(yt_utility):
            if callable(getattr(yt_utility, method_name)) and not method_name[0].isupper() \
                    and not method_name[0] == '_' \
                    and not method_name == 'register_callbacks'\
                    and not method_name[:3] == 'cmd'\
                    and not method_name == 'quit':
                gs.plugin_callbacks.register_callback(
                    f'{self.plugin_name}|{method_name}|clbk',
                    getattr(yt_utility, method_name)
                )

    def cmd_ytsearch(self, data):
        pass

    def cmd_ytplay(self, data):
        pass

    def cmd_ytplaylist(self, data):
        if gs.vlc_interface.check_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]):
            gs.vlc_interface.set_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        all_data = data.message.strip().split(' ', 1)
        sender = gs.mumble_inst.users[data.actor]['name']
        stripped_url = BeautifulSoup(all_data[1], features='html.parser').get_text()

        all_song_data = yt_utility.get_playlist_info(stripped_url)
        if all_song_data is None:
            return

        for i, song_data in enumerate(all_song_data):
            track_obj = TrackInfo(
                uri=song_data['main_url'],
                name=song_data['main_title'],
                sender=sender,
                duration=str(timedelta(seconds=int(song_data['duration']))) if int(song_data['duration']) > 0 else -1,
                track_type=TrackType.STREAM,
                track_id=song_data['main_id'],
                alt_uri=song_data['std_url'],
                image_uri=f"{dir_utils.get_temp_med_dir()}/{self.plugin_name}/{song_data['main_id']}",
                quiet=False
            )
            gs.vlc_interface.enqueue_track(
                track_obj=track_obj,
                to_front=False
            )
        gs.vlc_interface.play()

    def cmd_ytlink(self, data):
        if gs.vlc_interface.check_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]):
            gs.vlc_interface.set_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        all_data = data.message.strip().split(' ', 1)
        sender = gs.mumble_inst.users[data.actor]['name']
        stripped_url = BeautifulSoup(all_data[1], features='html.parser').get_text()
        if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
            if "playlist" in stripped_url or "list" in stripped_url:
                gs.gui_service.quick_gui(
                    "The given link was identified as a youtube playlist link!<br>Please use the playlist "
                    "command to add playlists to the queue!",
                    text_type='header',
                    box_align='left')
                return

            song_data = yt_utility.get_video_info(stripped_url)
            if song_data is None:
                gs.gui_service.quick_gui(
                    "ERROR: The youtube video information could not be retrieved.",
                    text_type='header',
                    box_align='left')
                return
            # song_data['main_url'] = stripped_url
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
            gs.vlc_interface.enqueue_track(
                track_obj=track_obj,
                to_front=False
            )
            gs.vlc_interface.play()

    def cmd_ytlinkfront(self, data):
        if gs.vlc_interface.check_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]):
            gs.vlc_interface.set_dni(self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        all_data = data.message.strip().split(' ', 1)
        sender = gs.mumble_inst.users[data.actor]['name']
        stripped_url = BeautifulSoup(all_data[1], features='html.parser').get_text()
        if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
            if "playlist" in stripped_url or "list" in stripped_url:
                gs.gui_service.quick_gui(
                    "The given link was identified as a youtube playlist link!<br>Please use the playlist "
                    "command to add playlists to the queue!",
                    text_type='header',
                    box_align='left')
                return

            song_data = yt_utility.get_video_info(stripped_url)
            if song_data is None:
                gs.gui_service.quick_gui(
                    "ERROR: The youtube video information could not be retrieved.",
                    text_type='header',
                    box_align='left')
                return
            # song_data['main_url'] = stripped_url
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
            gs.vlc_interface.enqueue_track(
                track_obj=track_obj,
                to_front=True
            )
            gs.vlc_interface.play()

    '''

        if command == "youtube":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return

            if not gs.audio_dni[0]:
                gs.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
            else:
                if gs.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                    rprint(
                        f'An audio plugin is using the audio thread with no interruption mode enabled. [{gs.audio_dni[1]}]')
                    gs.gui_service.quick_gui(
                        "An audio plugin is using the audio thread with no interruption mode enabled.",
                        text_type='header',
                        box_align='left')
                    return
            try:
                search_term = message_parse[1]
            except IndexError:
                return

            YH.all_searches = YM.get_vid_list(search_term, int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_SEARCH_LEN]))
            search_results = YM.get_choices(YH.all_searches)
            if not search_results:
                gs.gui_service.quick_gui(
                    f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>No search results found.</font>",
                    text_type='header',
                    box_align='left',
                    text_align='left')
                return
            gs.gui_service.quick_gui(
                f"{search_results}\nWhich one would you like to play?",
                text_type='header',
                box_align='left',
                text_align='left')
            log(INFO, "Displayed youtube search results.", origin=L_COMMAND)
            YH.can_play = True

        elif command == "play":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if YH.can_play:
                if not gs.audio_dni[0]:
                    gs.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
                else:
                    if gs.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                        rprint(
                            f'An audio plugin is using the audio thread with no interruption mode enabled. [{gs.audio_dni[1]}]')
                        gs.gui_service.quick_gui(
                            "An audio plugin is using the audio thread with no interruption mode enabled.",
                            text_type='header',
                            box_align='left')
                        return

                if YH.queue_instance.is_full():
                    gs.gui_service.quick_gui(
                        "The youtube queue is full!",
                        text_type='header',
                        box_align='left')
                    return

                all_messages = message[1:].split()
                if len(all_messages) == 1:
                    song_data = YM.download_song_name(
                        "https://www.youtube.com" + YH.all_searches[0]['href'])
                    if song_data is None:
                        gs.gui_service.quick_gui(
                            f"The chosen video is too long. The maximum video length is {(YH.max_track_duration / 60)} minutes",
                            text_type='header',
                            box_align='left')
                        return
                    # song_data['main_url'] = "https://www.youtube.com" + YH.all_searches[0]['href']
                    gs.gui_service.quick_gui(
                        f"Automatically chosen: {YH.all_searches[0]['title']}",
                        text_type='header',
                        box_align='left')
                    YH.can_play = False
                    YH.queue_instance.insert(song_data)
                    if not YH.is_playing:
                        YM.download_next()
                        YM.play_audio()
                elif len(all_messages) == 2:
                    if 9 >= int(all_messages[1]) >= 0:
                        song_data = YM.download_song_name(
                            "https://www.youtube.com" + YH.all_searches[int(all_messages[1])]['href'])
                        if song_data is None:
                            gs.gui_service.quick_gui(
                                f"The chosen video is too long. The maximum video length is {(YH.max_track_duration / 60)} minutes",
                                text_type='header',
                                box_align='left')
                            return
                        # song_data['main_url'] = "https://www.youtube.com" + YH.all_searches[int(all_messages[1])]['href']
                        gs.gui_service.quick_gui(
                            f"You've chosen: {YH.all_searches[int(all_messages[1])]['title']}",
                            text_type='header',
                            box_align='left')
                        YH.can_play = False
                    else:
                        gs.gui_service.quick_gui(
                            "Invalid choice! Valid Range [0-9]",
                            text_type='header',
                            box_align='left')
                        YH.can_play = False
                        return
                    YH.queue_instance.insert(song_data)
                    if not YH.is_playing:
                        YM.download_next()
                        YM.play_audio()
                elif len(all_messages) == 3:
                    if 9 >= int(all_messages[1]) >= 0:
                        song_data = YM.download_song_name(
                            "https://www.youtube.com" + YH.all_searches[int(all_messages[1])]['href'])
                        if song_data is None:
                            gs.gui_service.quick_gui(
                                f"The chosen video is too long. The maximum video length is {(YH.max_track_duration / 60)} minutes",
                                text_type='header',
                                box_align='left')
                            return
                        #song_data['main_url'] = "https://www.youtube.com" + YH.all_searches[int(all_messages[1])]['href']
                        gs.gui_service.quick_gui(
                            f"You've chosen: {YH.all_searches[int(all_messages[1])]['title']}",
                            text_type='header',
                            box_align='left')
                        YH.can_play = False
                    else:
                        gs.gui_service.quick_gui(
                            "Invalid choice! Valid Range [0-9]",
                            text_type='header',
                            box_align='left')
                        YH.can_play = False
                        return
                    count = int(all_messages[2])
                    for i in range(count):
                        YH.queue_instance.insert(song_data)
                    if not YH.is_playing:
                        YM.download_next()
                        YM.play_audio()

    '''
