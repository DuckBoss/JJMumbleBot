import warnings
from bs4 import BeautifulSoup
import helpers.queue_handler as qh
import plugins.youtube.youtube_helper as YM
import privileges as pv
import utils
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print, reg_print
from plugins.youtube.youtube_helper import YoutubeHelper as YH
from templates.plugin_template import PluginBase


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
                        <b>!youtube/!yt 'search_term'</b>: Searches youtube for a song/video.<br>\
                        <b>!play/!p 'item_number' 'item_count'(optional)</b>: Plays the selected song from youtube.<br>\
                        <b>!link 'youtube_link'</b>: Plays the given youtube link.<br>\
                        <b>!stop</b>: Stops the currently playing track and clears the queue.<br>\
                        <b>!shuffle</b>: Shuffles all the tracks in the queue.<br>\
                        <b>!volume/!v '0..1'</b>: Sets the bot audio volume.<br>\
                        <b>!replay/!rp</b>: Replays the last played audio track.<br>\
                        <b>!next/!skip</b>: Goes to the next song in the queue.<br>\
                        <b>!skipto 'number'</b>: Skips ahead in the queue by the provided number.<br>\
                        <b>!remove 'number'</b>: Removes the track in the queue by the provided number.<br>\
                        <b>!queue/!q</b>: Displays the youtube queue.<br>\
                        <b>!song</b>: Shows currently playing track.<br>\
                        <b>!clear</b>: Clears the current youtube queue.<br>"
    plugin_version = "2.0.0"
    priv_path = "youtube/youtube_privileges.csv"

    sound_board_plugin = None

    def __init__(self):
        debug_print("Music Plugin Initialized...")
        super().__init__()
        warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
        YH.volume = float(GM.cfg['Plugin_Settings']['Youtube_DefaultVolume'])
        YH.max_queue_size = int(GM.cfg['Plugin_Settings']['Youtube_MaxQueueLength'])
        YH.max_track_duration = int(GM.cfg['Plugin_Settings']['Youtube_MaxVideoLength'])
        YH.autoplay = GM.cfg.getboolean('Plugin_Settings', 'Youtube_AutoPlay')
        YH.queue_instance = qh.QueueHandler(YH.max_queue_size)

    def set_sound_board_plugin(self, sb_plugin):
        self.sound_board_plugin = sb_plugin

    def process_command(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]

        if command == "song":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if YH.current_song_info is not None:
                GM.gui.quick_gui_img(f"{utils.get_temporary_img_dir()}",
                                     f"{YH.current_song_info['img_id']}",
                                     caption=f"Now playing: {YH.current_song_info['main_title']}",
                                     format=True,
                                     img_size=32768)
            else:
                GM.gui.quick_gui(
                    f"{utils.get_bot_name()} is not playing anything right now.",
                    text_type='header',
                    box_align='left')
            return

        elif command == "shuffle":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if YH.music_thread is not None:
                if not YH.queue_instance.is_empty():
                    YH.queue_instance.shuffle()
                    YM.download_next()
                    GM.gui.quick_gui(
                        "The youtube queue has been shuffled.",
                        text_type='header',
                        box_align='left')
                    return

        elif command == "next":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            YM.next()
            return

        elif command == "remove":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if YH.music_thread is not None:
                if YH.queue_instance.is_empty():
                    GM.gui.quick_gui(
                        "The youtube queue is empty, so I can't remove tracks.",
                        text_type='header',
                        box_align='left')
                    return
                rem_val = int(message[1:].split(' ', 1)[1])
                if rem_val > YH.queue_instance.size() - 1 or rem_val < 0:
                    GM.gui.quick_gui(
                        f"You can't remove tracks beyond the length of the current queue.",
                        text_type='header',
                        box_align='left')
                    return
                removed_item = YH.queue_instance.remove(rem_val)
                GM.gui.quick_gui(
                    f"Removed track: [{rem_val}]-{removed_item['main_title']} from the queue.",
                    text_type='header',
                    box_align='left')
                return

        elif command == "skipto":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            skip_val = int(message[1:].split(' ', 1)[1])
            YM.skipto(skip_val)
            return

        elif command == "stop":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if YH.music_thread is not None:
                GM.gui.quick_gui(
                    "Stopping youtube audio thread.",
                    text_type='header',
                    box_align='left')
                YH.queue_instance.clear()
                YM.stop_audio()
                YH.queue_instance = qh.QueueHandler(YH.max_queue_size)
                GM.logger.info("The youtube audio thread was stopped.")
                return
            return

        elif command == "clear":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            reg_print("Clearing youtube queue.")
            YM.clear_queue()
            GM.gui.quick_gui(
                "Cleared youtube queue.",
                text_type='header',
                box_align='left')
            GM.logger.info("The youtube queue was cleared.")
            return

        elif command == "max_duration":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                new_max = int(message[1:].split(' ', 1)[1])
                YM.set_max_track_duration(new_max)
                GM.gui.quick_gui(
                    f"Set youtube track max duration to {YH.max_track_duration}",
                    text_type='header',
                    box_align='left')
                GM.logger.info(f"The youtube track max duration was set to {YH.max_track_duration}")
            except IndexError:
                GM.gui.quick_gui(
                    f"Current youtube track max duration: {YH.max_track_duration}",
                    text_type='header',
                    box_align='left')
                return

        elif command == "volume":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                GM.gui.quick_gui(
                    f"Current youtube volume: {YH.volume}",
                    text_type='header',
                    box_align='left')
                return

            if vol > 1:
                GM.gui.quick_gui(
                    "Invalid Volume Input: [0-1]",
                    text_type='header',
                    box_align='left')
                return
            if vol < 0:
                GM.gui.quick_gui(
                    "Invalid Volume Input: [0-1]",
                    text_type='header',
                    box_align='left')
                return
            YH.volume = vol
            GM.gui.quick_gui(
                f"Set volume to {YH.volume}",
                text_type='header',
                box_align='left')
            GM.logger.info(f"The youtube audio volume was changed to {YH.volume}")
            return

        elif command == "youtube":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                search_term = message_parse[1]
            except IndexError:
                return

            YH.all_searches = YM.get_search_results(search_term)
            search_results = YM.get_choices(YH.all_searches)

            GM.gui.quick_gui(
                f"{search_results}\nWhich one would you like to play?",
                text_type='header',
                box_align='left',
                text_align='left')
            YH.can_play = True
            return

        elif command == "queue":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            queue_results = YM.get_queue()
            if queue_results is not None:
                cur_text = ""
                for i, item in enumerate(queue_results):
                    cur_text += f"{item}"
                    if i % 50 == 0 and i != 0:
                        GM.gui.quick_gui(
                            f"{cur_text}",
                            text_type='header',
                            box_align='left',
                            text_align='left')
                        cur_text = ""
                if cur_text != "":
                    GM.gui.quick_gui(
                        f"{cur_text}",
                        text_type='header',
                        box_align='left',
                        text_align='left')
                return
            else:
                GM.gui.quick_gui(
                    "The youtube queue is empty.",
                    text_type='header',
                    box_align='left')
            return

        elif command == "playlist":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if len(message_parse) == 2:
                stripped_url = BeautifulSoup(message_parse[1], features='html.parser').get_text()
                if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
                    if YH.queue_instance.is_full():
                        GM.gui.quick_gui(
                            "The youtube queue is full!",
                            text_type='header',
                            box_align='left')
                        return
                    all_song_data = YM.download_playlist(stripped_url)
                    if all_song_data is None:
                        return

                    self.sound_board_plugin.clear_audio_thread()
                    for i, song_data in enumerate(all_song_data):
                        YH.queue_instance.insert(song_data)

                    GM.gui.quick_gui(
                        f"Playlist generated: {stripped_url}",
                        text_type='header',
                        box_align='left')
                    if not YH.is_playing:
                        YM.download_next()
                        YM.play_audio()
                    return
            else:
                GM.gui.quick_gui(
                    "The given link was not identified as a youtube video link!",
                    text_type='header',
                    box_align='left')
                return

        elif command == "link":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if len(message_parse) == 2:
                stripped_url = BeautifulSoup(message_parse[1], features='html.parser').get_text()
                if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
                    if YH.queue_instance.is_full():
                        GM.gui.quick_gui(
                            "The youtube queue is full!",
                            text_type='header',
                            box_align='left')
                        return
                    song_data = YM.download_song_name(stripped_url)
                    if song_data is None:
                        GM.gui.quick_gui(
                            "ERROR: The chosen stream was either too long or a live stream.",
                            text_type='header',
                            box_align='left')
                        return
                    song_data['main_url'] = stripped_url

                    self.sound_board_plugin.clear_audio_thread()
                    YH.queue_instance.insert(song_data)

                    GM.gui.quick_gui(
                        f"Added to queue: {stripped_url}",
                        text_type='header',
                        box_align='left')
                    if not YH.is_playing:
                        YM.download_next()
                        YM.play_audio()
                    return
                else:
                    GM.gui.quick_gui(
                        "The given link was not identified as a youtube video link!",
                        text_type='header',
                        box_align='left')
                    return

        elif command == "play":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if YH.can_play:
                if YH.queue_instance.is_full():
                    GM.gui.quick_gui(
                        "The youtube queue is full!",
                        text_type='header',
                        box_align='left')
                    return
                self.sound_board_plugin.clear_audio_thread()

                if len(all_messages) == 1:
                    song_data = YM.download_song_name(
                        "https://www.youtube.com" + YH.all_searches[0]['href'])
                    if song_data is None:
                        GM.gui.quick_gui(
                            f"The chosen video is too long. The maximum video length is {(YH.max_track_duration/60)} minutes",
                            text_type='header',
                            box_align='left')
                        return
                    song_data['main_url'] = "https://www.youtube.com" + YH.all_searches[0]['href']
                    GM.gui.quick_gui(
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
                            utils.echo(utils.get_my_channel(),
                                       f"The chosen video is too long. The maximum video length is {(YH.max_track_duration/60)} minutes")
                            return
                        song_data['main_url'] = "https://www.youtube.com" + YH.all_searches[int(all_messages[1])]['href']
                        GM.gui.quick_gui(
                            f"You've chosen: {YH.all_searches[int(all_messages[1])]['title']}",
                            text_type='header',
                            box_align='left')
                        YH.can_play = False
                    else:
                        GM.gui.quick_gui(
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
                            GM.gui.quick_gui(
                                f"The chosen video is too long. The maximum video length is {(YH.max_track_duration/60)} minutes",
                                text_type='header',
                                box_align='left')
                            return
                        song_data['main_url'] = "https://www.youtube.com" + YH.all_searches[int(all_messages[1])]['href']
                        GM.gui.quick_gui(
                            f"You've chosen: {YH.all_searches[int(all_messages[1])]['title']}",
                            text_type='header',
                            box_align='left')
                        YH.can_play = False
                    else:
                        GM.gui.quick_gui(
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
            return

        elif command == "replay":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if YH.music_thread is not None:
                if YH.current_song is not None and YH.current_song_info is not None:
                    YH.queue_instance.insert_priority(YH.current_song_info)
                    YM.stop_audio()
                    YM.download_next()
                    YM.play_audio()
            else:
                GM.gui.quick_gui(
                    "There is no track available to replay.",
                    text_type='header',
                    box_align='left')
                return
            return

    def clear_audio_plugin(self):
        if not YH.is_playing:
            YM.clear_audio_thread()
            return True
        return False

    def plugin_test(self):
        debug_print("Youtube Plugin self-test callback.")

    def quit(self):
        YM.stop_audio()
        YH.exit_flag = True
        debug_print("Exiting Youtube Plugin...")

    def help(self):
        return self.help_data

    def is_audio_plugin(self):
        return True

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
