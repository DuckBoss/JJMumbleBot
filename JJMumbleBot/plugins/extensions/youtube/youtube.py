from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils import runtime_utils
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.youtube.resources.strings import *
from JJMumbleBot.plugins.extensions.youtube.utility.youtube_helper import YoutubeHelper as YH
from JJMumbleBot.plugins.extensions.youtube.utility import youtube_helper as YM
import warnings
import os
from JJMumbleBot.lib.helpers import queue_handler as qh
from bs4 import BeautifulSoup


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_DIR][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
        YH.yt_metadata = self.metadata
        YH.volume = float(self.metadata[C_PLUGIN_SETTINGS][P_YT_DEF_VOL])
        YH.max_queue_size = int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_QUE_LEN])
        YH.max_track_duration = int(self.metadata[C_PLUGIN_SETTINGS][P_YT_MAX_VID_LEN])
        YH.autoplay = self.metadata.getboolean(C_PLUGIN_SETTINGS, P_YT_AUTO_PLAY, fallback=True)
        YH.queue_instance = qh.QueueHandler(YH.max_queue_size)
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def get_metadata(self):
        return self.metadata

    def quit(self):
        YM.stop_audio()
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/youtube')
        YH.exit_flag = True
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "song":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if YH.current_song_info is not None:
                GS.gui_service.quick_gui_img(f"{dir_utils.get_temp_med_dir()}/youtube",
                                             f"{YH.current_song_info['img_id']}",
                                             caption=f"Now playing: {YH.current_song_info['main_title']}",
                                             format=True,
                                             img_size=32768)
                log(INFO, "Displayed current song in the youtube plugin.", origin=L_COMMAND)
            else:
                GS.gui_service.quick_gui(
                    f"{runtime_utils.get_bot_name()}({self.plugin_name}) is not playing anything right now.",
                    text_type='header',
                    box_align='left')

        elif command == "autoplay":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if YH.autoplay:
                YH.autoplay = False
                GS.gui_service.quick_gui(
                    "Autoplay has been disabled.",
                    text_type='header',
                    box_align='left')
                log(INFO, "Autoplay has been disabled in the youtube plugin.", origin=L_COMMAND)
            else:
                YH.autoplay = True
                GS.gui_service.quick_gui(
                    "Autoplay has been enabled.",
                    text_type='header',
                    box_align='left')
                log(INFO, "Autoplay has been enabled in the youtube plugin.", origin=L_COMMAND)

        elif command == "shuffle":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if GS.audio_inst is not None:
                if not YH.queue_instance.is_empty():
                    YH.queue_instance.shuffle()
                    YM.download_next()
                    GS.gui_service.quick_gui(
                        "The youtube queue has been shuffled.",
                        text_type='header',
                        box_align='left')
                    log(INFO, "The youtube audio queue was shuffled.", origin=L_COMMAND)
                    return

        elif command == "next":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if not GS.audio_dni[0]:
                GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
            else:
                if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                    rprint(
                        f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[0]}|{GS.audio_dni[1]}]')
                    GS.gui_service.quick_gui(
                        "An audio plugin is using the audio thread with no interruption mode enabled.",
                        text_type='header',
                        box_align='left')
                    return
            YM.next_track()

        elif command == "removetrack":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if GS.audio_inst is not None:
                if YH.queue_instance.is_empty():
                    GS.gui_service.quick_gui(
                        "The youtube queue is empty, so I can't remove tracks.",
                        text_type='header',
                        box_align='left')
                    return
                rem_val = int(message[1:].split(' ', 1)[1])
                if rem_val > YH.queue_instance.size() - 1 or rem_val < 0:
                    GS.gui_service.quick_gui(
                        f"You can't remove tracks beyond the length of the current queue.",
                        text_type='header',
                        box_align='left')
                    return
                removed_item = YH.queue_instance.remove(rem_val)
                GS.gui_service.quick_gui(
                    f"Removed track: [{rem_val}]-{removed_item['main_title']} from the queue.",
                    text_type='header',
                    box_align='left')
                log(INFO, f"Removed track #{rem_val} from the youtube audio queue.", origin=L_COMMAND)
                return

        elif command == "skipto":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            skip_val = int(message[1:].split(' ', 1)[1])
            YM.skipto(skip_val)
            log(INFO, f"The youtube audio queue skipped to track #{skip_val}.", origin=L_COMMAND)

        elif command == "stop":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if GS.audio_inst is not None:
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
                GS.gui_service.quick_gui(
                    "Stopping youtube audio thread.",
                    text_type='header',
                    box_align='left')
                YH.queue_instance.clear()
                YM.stop_audio()
                dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/youtube')
                YH.queue_instance = qh.QueueHandler(YH.max_queue_size)
                log(INFO, "The youtube audio thread was stopped.", origin=L_COMMAND)
                return

        elif command == "clear":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            rprint("Clearing youtube queue.")
            YM.clear_queue()
            GS.gui_service.quick_gui(
                "Cleared youtube queue.",
                text_type='header',
                box_align='left')
            log(INFO, "The youtube queue was cleared.", origin=L_COMMAND)

        elif command == "volume":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                GS.gui_service.quick_gui(
                    f"Current youtube volume: {YH.volume}",
                    text_type='header',
                    box_align='left')
                return

            if vol > 1 or vol < 0:
                GS.gui_service.quick_gui(
                    "Invalid Volume Input: [0-1]",
                    text_type='header',
                    box_align='left')
                return
            YH.volume = vol
            GS.gui_service.quick_gui(
                f"Set volume to {YH.volume}",
                text_type='header',
                box_align='left')
            log(INFO, f"The youtube audio volume was changed to {YH.volume}.", origin=L_COMMAND)

        elif command == "youtube":
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

            try:
                search_term = message_parse[1]
            except IndexError:
                return

            YH.all_searches = YM.get_search_results(search_term)
            search_results = YM.get_choices(YH.all_searches)
            GS.gui_service.quick_gui(
                f"{search_results}\nWhich one would you like to play?",
                text_type='header',
                box_align='left',
                text_align='left')
            log(INFO, "Displayed youtube search results.", origin=L_COMMAND)
            YH.can_play = True

        elif command == "queue":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            queue_results = YM.get_queue()
            if queue_results is not None:
                cur_text = ""
                for i, item in enumerate(queue_results):
                    cur_text += f"{item}"
                    if i % 50 == 0 and i != 0:
                        GS.gui_service.quick_gui(
                            f"{cur_text}",
                            text_type='header',
                            box_align='left',
                            text_align='left')
                        cur_text = ""
                if cur_text != "":
                    GS.gui_service.quick_gui(
                        f"{cur_text}",
                        text_type='header',
                        box_align='left',
                        text_align='left')
                log(INFO, "Displayed current youtube queue.", origin=L_COMMAND)
            else:
                GS.gui_service.quick_gui(
                    "The youtube queue is empty.",
                    text_type='header',
                    box_align='left')

        elif command == "playlist":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if len(message_parse) == 2:
                if not GS.audio_dni[0]:
                    GS.audio_dni = (True, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
                else:
                    if GS.audio_dni[1] != self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                        rprint(
                            f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[0]}|{GS.audio_dni[1]}]')
                        GS.gui_service.quick_gui(
                            "An audio plugin is using the audio thread with no interruption mode enabled.",
                            text_type='header',
                            box_align='left')
                        return

                stripped_url = BeautifulSoup(message_parse[1], features='html.parser').get_text()
                if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
                    if YH.queue_instance.is_full():
                        GS.gui_service.quick_gui(
                            "The youtube queue is full!",
                            text_type='header',
                            box_align='left')
                        return
                    all_song_data = YM.download_playlist(stripped_url)
                    if all_song_data is None:
                        return

                    for i, song_data in enumerate(all_song_data):
                        YH.queue_instance.insert(song_data)

                    GS.gui_service.quick_gui(
                        f'Playlist Generated:<br><a href="{stripped_url}">{stripped_url}</a>',
                        text_type='header',
                        box_align='left')
                    log(INFO, f"Generated playlist: {stripped_url}", origin=L_COMMAND)
                    if not YH.is_playing:
                        YM.download_next()
                        YM.play_audio()
                    return
            else:
                GS.gui_service.quick_gui(
                    "The given link was not identified as a youtube video link!",
                    text_type='header',
                    box_align='left')
                return

        elif command == "linkfront":
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

            if len(message_parse) == 2:
                stripped_url = BeautifulSoup(message_parse[1], features='html.parser').get_text()
                if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
                    if YH.queue_instance.is_full():
                        GS.gui_service.quick_gui(
                            "The youtube queue is full!",
                            text_type='header',
                            box_align='left')
                        return
                    song_data = YM.download_song_name(stripped_url)
                    if song_data is None:
                        GS.gui_service.quick_gui(
                            "ERROR: The chosen stream was either too long or a live stream.",
                            text_type='header',
                            box_align='left')
                        return
                    song_data['main_url'] = stripped_url

                    # self.sound_board_plugin.clear_audio_thread()
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
                    YH.queue_instance.insert_priority(song_data)

                    GS.gui_service.quick_gui(
                        f"Added to front of queue: {stripped_url}",
                        text_type='header',
                        box_align='left')
                    GS.log_service.info("Direct link added to the front of the youtube queue.")
                    if not YH.is_playing:
                        YM.download_next()
                        YM.play_audio()
                else:
                    GS.gui_service.quick_gui(
                        "The given link was not identified as a youtube video link!",
                        text_type='header',
                        box_align='left')

        elif command == "link":
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

            if len(message_parse) == 2:
                stripped_url = BeautifulSoup(message_parse[1], features='html.parser').get_text()
                if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
                    if YH.queue_instance.is_full():
                        GS.gui_service.quick_gui(
                            "The youtube queue is full!",
                            text_type='header',
                            box_align='left')
                        return
                    song_data = YM.download_song_name(stripped_url)
                    if song_data is None:
                        GS.gui_service.quick_gui(
                            "ERROR: The chosen stream was either too long or a live stream.",
                            text_type='header',
                            box_align='left')
                        return
                    song_data['main_url'] = stripped_url

                    # self.sound_board_plugin.clear_audio_thread()
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
                    YH.queue_instance.insert(song_data)

                    GS.gui_service.quick_gui(
                        f"Added to queue: {stripped_url}",
                        text_type='header',
                        box_align='left')
                    GS.log_service.info("Direct link added to youtube queue.")
                    if not YH.is_playing:
                        YM.download_next()
                        YM.play_audio()
                else:
                    GS.gui_service.quick_gui(
                        "The given link was not identified as a youtube video link!",
                        text_type='header',
                        box_align='left')

        elif command == "loop":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            YH.loop_song = not YH.loop_song
            rprint(
                f'{"Enabled" if YH.loop_song is True else "Disabled"} {self.plugin_name} loop mode.')
            GS.gui_service.quick_gui(
                f'{"Enabled" if YH.loop_song is True else "Disabled"} {self.plugin_name} loop mode.',
                text_type='header',
                box_align='left')
            if GS.audio_dni[1] == self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME] and GS.audio_dni[0] is True:
                if GS.audio_inst is not None:
                    if YH.current_song is not None and YH.current_song_info is not None:
                        YH.queue_instance.insert_priority(YH.current_song_info)
                        YM.stop_audio()
                        YM.download_next()
                        YM.play_audio()

        elif command == "play":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if YH.can_play:
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

                if YH.queue_instance.is_full():
                    GS.gui_service.quick_gui(
                        "The youtube queue is full!",
                        text_type='header',
                        box_align='left')
                    return

                all_messages = message[1:].split()
                if len(all_messages) == 1:
                    song_data = YM.download_song_name(
                        "https://www.youtube.com" + YH.all_searches[0]['href'])
                    if song_data is None:
                        GS.gui_service.quick_gui(
                            f"The chosen video is too long. The maximum video length is {(YH.max_track_duration / 60)} minutes",
                            text_type='header',
                            box_align='left')
                        return
                    song_data['main_url'] = "https://www.youtube.com" + YH.all_searches[0]['href']
                    GS.gui_service.quick_gui(
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
                            GS.gui_service.quick_gui(
                                f"The chosen video is too long. The maximum video length is {(YH.max_track_duration / 60)} minutes",
                                text_type='header',
                                box_align='left')
                            return
                        song_data['main_url'] = "https://www.youtube.com" + YH.all_searches[int(all_messages[1])][
                            'href']
                        GS.gui_service.quick_gui(
                            f"You've chosen: {YH.all_searches[int(all_messages[1])]['title']}",
                            text_type='header',
                            box_align='left')
                        YH.can_play = False
                    else:
                        GS.gui_service.quick_gui(
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
                            GS.gui_service.quick_gui(
                                f"The chosen video is too long. The maximum video length is {(YH.max_track_duration / 60)} minutes",
                                text_type='header',
                                box_align='left')
                            return
                        song_data['main_url'] = "https://www.youtube.com" + YH.all_searches[int(all_messages[1])][
                            'href']
                        GS.gui_service.quick_gui(
                            f"You've chosen: {YH.all_searches[int(all_messages[1])]['title']}",
                            text_type='header',
                            box_align='left')
                        YH.can_play = False
                    else:
                        GS.gui_service.quick_gui(
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

        elif command == "replay":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if GS.audio_inst is not None:
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

                if YH.current_song is not None and YH.current_song_info is not None:
                    YH.queue_instance.insert_priority(YH.current_song_info)
                    YM.stop_audio()
                    YM.download_next()
                    YM.play_audio()
            else:
                GS.gui_service.quick_gui(
                    "There is no track available to replay.",
                    text_type='header',
                    box_align='left')
                return
