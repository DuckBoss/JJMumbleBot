from templates.plugin_template import PluginBase
import privileges as pv
import utils
import youtube_dl
import urllib.request
from bs4 import BeautifulSoup
import os
import subprocess as sp
import time
import audioop
import helpers.queue_handler as qh
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print, reg_print
import warnings


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Youtube Plugin Help <font color='red'>#####</font></b><br> \
                        All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
                        <b>!youtube/!yt 'search_term'</b>: Searches youtube for a song/video.<br>\
                        <b>!play/!p 'item_number' 'item_count'(optional)</b>: Plays the selected song from youtube.<br>\
                        <b>!link 'youtube_link'</b>: Plays the given youtube link.<br>\
                        <b>!stop</b>: Stops the currently playing track and clears the queue.<br>\
                        <b>!volume/!v '0..1'</b>: Sets the bot audio volume.<br>\
                        <b>!replay/!rp</b>: Replays the last played audio track.<br>\
                        <b>!next/!skip</b>: Goes to the next song in the queue.<br>\
                        <b>!queue/!q</b>: Displays the youtube queue.<br>\
                        <b>!song</b>: Shows currently playing track.<br>\
                        <b>!clear</b>: Clears the current youtube queue.<br>"
    plugin_version = "1.7.1"
    priv_path = "youtube/youtube_privileges.csv"

    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192', }],
        'logger': GM.logger
    }

    queue_instance = None
    all_searches = None
    can_play = False
    is_playing = False
    current_song = None
    current_song_info = None
    music_thread = None
    exit_flag = False
    # default volume
    volume = 0.5

    sound_board_plugin = None

    # max number of tracks in the queue.
    max_queue_size = 25
    # max track duration in seconds.
    max_track_duration = 900

    def __init__(self):
        debug_print("Music Plugin Initialized...")
        super().__init__()
        warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
        self.volume = float(GM.cfg['Plugin_Settings']['Youtube_DefaultVolume'])
        self.max_queue_size = int(GM.cfg['Plugin_Settings']['Youtube_MaxQueueLength'])
        self.max_track_duration = int(GM.cfg['Plugin_Settings']['Youtube_MaxVideoLength'])
        self.queue_instance = qh.QueueHandler(self.max_queue_size)

    def set_sound_board_plugin(self, sb_plugin):
        self.sound_board_plugin = sb_plugin

    def set_max_track_duration(self, new_max):
        self.max_track_duration = new_max

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]

        if command == "song":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            if self.current_song_info is not None:
                utils.echo(utils.get_my_channel(mumble),
                           f"Now playing: {self.current_song_info['main_title']}")
            else:
                utils.echo(utils.get_my_channel(mumble),
                           f"{utils.get_bot_name()} is not playing anything right now.")
            return

        elif command == "next":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            if self.music_thread is not None:
                if self.queue_instance.is_empty():
                    utils.echo(utils.get_my_channel(mumble),
                               "The youtube queue is empty, so I can't go to the next song.")
                    return
                utils.echo(utils.get_my_channel(mumble),
                           "Going to next available track...")
                GM.logger.info("The youtube audio queue moved to the next available track.")
                self.stop_audio()
                self.audio_loop(mumble)
                return
            return

        elif command == "stop":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            if self.music_thread is not None:
                utils.echo(utils.get_my_channel(mumble),
                           "Stopping youtube audio thread...")
                self.queue_instance.clear()
                self.stop_audio()
                self.queue_instance = qh.QueueHandler(self.max_queue_size)
                GM.logger.info("The youtube audio thread was stopped.")
                return
            return

        elif command == "clear":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            reg_print("Clearing youtube queue.")
            self.clear_queue()
            utils.echo(utils.get_my_channel(mumble),
                           "Cleared youtube queue.")
            GM.logger.info("The youtube queue was cleared.")
            return

        elif command == "max_duration":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                new_max = int(message[1:].split(' ', 1)[1])
                self.set_max_track_duration(new_max)
                utils.echo(utils.get_my_channel(mumble),
                           f"Set youtube track max duration to {self.max_track_duration}")
                GM.logger.info(f"The youtube track max duration was set to {self.max_track_duration}")
            except IndexError:
                utils.echo(utils.get_my_channel(mumble),
                           f"Current youtube track max duration: {self.max_track_duration}")
                return

        elif command == "volume":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                utils.echo(utils.get_my_channel(mumble),
                           f"Current youtube volume: {self.volume}")
                return

            if vol > 1:
                utils.echo(utils.get_my_channel(mumble),
                           "Invalid Volume Input: [0-1]")
                return
            if vol < 0:
                utils.echo(utils.get_my_channel(mumble),
                           "Invalid Volume Input: [0-1]")
                return
            self.volume = vol
            utils.echo(utils.get_my_channel(mumble),
                       f"Set volume to {self.volume}")
            GM.logger.info(f"The youtube audio volume was changed to {self.volume}")
            return

        elif command == "youtube":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            try:
                search_term = message_parse[1]
            except IndexError:
                return
            
            self.all_searches = self.get_search_results(search_term)
            search_results = self.get_choices(self.all_searches)

            utils.echo(utils.get_my_channel(mumble),
                       f"{search_results}\nWhich one would you like to play?")
            self.can_play = True
            return

        elif command == "queue":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            queue_results = self.get_queue()
            if queue_results is not None:
                utils.echo(utils.get_my_channel(mumble),
                           f"<br>{self.get_queue()}")
                return
            else:
                utils.echo(utils.get_my_channel(mumble),
                           "The youtube queue is empty.")
            return

        elif command == "link":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            if len(message_parse) == 2:
                stripped_url = BeautifulSoup(message_parse[1], features='html.parser').get_text()
                if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
                    if self.queue_instance.is_full():
                        utils.echo(utils.get_my_channel(mumble),
                                   "The youtube queue is full!")
                        return
                    song_data = self.download_song_name(stripped_url)
                    if song_data is None:
                        utils.echo(utils.get_my_channel(mumble),
                           "ERROR: The chosen stream was either too long or a live stream.")
                        return
                    song_data['main_id'] = stripped_url
                    utils.echo(utils.get_my_channel(mumble),
                                       f"Stream link given: {stripped_url}")
                    self.sound_board_plugin.clear_audio_thread()
                    self.queue_instance.insert(song_data)
                    self.audio_loop(mumble)
                    return
                else:
                    utils.echo(utils.get_my_channel(mumble),
                               "The given link was not identified as a youtube video link!")
                    return

        elif command == "play":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            if self.can_play:
                # self.stop_audio()
                if self.queue_instance.is_full():
                    utils.echo(utils.get_my_channel(mumble),
                               "The youtube queue is full!")
                    return
                self.sound_board_plugin.clear_audio_thread()

                if len(all_messages) == 1:
                    song_data = self.download_song_name(
                        "https://www.youtube.com" + self.all_searches[0]['href'])
                    if song_data is None:
                        utils.echo(utils.get_my_channel(mumble),
                           f"The chosen video is too long. The maximum video length is {(self.max_track_duration/60)} minutes")
                        return
                    song_data['main_id'] = "https://www.youtube.com" + self.all_searches[0]['href']
                    utils.echo(utils.get_my_channel(mumble),
                               f"Automatically chosen: {self.all_searches[0]['title']}")
                    self.can_play = False
                    self.queue_instance.insert(song_data)
                    self.audio_loop(mumble)
                elif len(all_messages) == 2:
                    if 9 >= int(all_messages[1]) >= 0:
                        song_data = self.download_song_name(
                            "https://www.youtube.com" + self.all_searches[int(all_messages[1])]['href'])
                        if song_data is None:
                            utils.echo(utils.get_my_channel(mumble), 
                                f"The chosen video is too long. The maximum video length is {(self.max_track_duration/60)} minutes")
                            return
                        song_data['main_id'] = "https://www.youtube.com" + self.all_searches[int(all_messages[1])]['href']
                        utils.echo(utils.get_my_channel(mumble),
                                   f"You've chosen: {self.all_searches[int(all_messages[1])]['title']}")
                        self.can_play = False
                    else:
                        utils.echo(utils.get_my_channel(mumble),
                               "Invalid choice! Valid Range [0-9]")
                        self.can_play = False
                        return
                    self.queue_instance.insert(song_data)
                    self.audio_loop(mumble)
                elif len(all_messages) == 3:
                    if 9 >= int(all_messages[1]) >= 0:
                        song_data = self.download_song_name(
                            "https://www.youtube.com" + self.all_searches[int(all_messages[1])]['href'])
                        if song_data is None:
                            utils.echo(utils.get_my_channel(mumble), 
                                f"The chosen video is too long. The maximum video length is {(self.max_track_duration/60)} minutes")
                            return
                        song_data['main_id'] = "https://www.youtube.com" + self.all_searches[int(all_messages[1])]['href']
                        utils.echo(utils.get_my_channel(mumble),
                                   f"You've chosen: {self.all_searches[int(all_messages[1])]['title']}")
                        self.can_play = False
                    else:
                        utils.echo(utils.get_my_channel(mumble),
                               "Invalid choice! Valid Range [0-9]")
                        self.can_play = False
                        return
                    count = int(all_messages[2])
                    for i in range(count):
                        self.queue_instance.insert(song_data)
                    self.audio_loop(mumble)
            return

        elif command == "replay":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            if self.music_thread is not None:
                if self.current_song is not None and self.current_song_info is not None:
                    if pv.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                        return
                    self.queue_instance.insert_priority(self.current_song_info)
                    self.stop_audio()
                    self.audio_loop(mumble)
            else:
                utils.echo(utils.get_my_channel(mumble),
                           "There is no track available to replay.")
                return
            return

    def clear_audio_thread(self):
        if self.music_thread is not None:
            debug_print("Stopping audio thread...")
            self.music_thread.terminate()
            self.music_thread.kill()
            self.music_thread = None
            self.is_playing = False

    def clear_audio_plugin(self):
        if not self.is_playing:
            self.clear_audio_thread()
            return True
        return False

    def stop_current(self):
        if self.music_thread is not None:
            self.current_song_info = None
            self.current_song = None
            self.is_playing = False

    def stop_audio(self):
        if self.music_thread is not None:
            debug_print("Stopping audio thread...")
            self.music_thread.terminate()
            self.music_thread.kill()
            self.music_thread = None
            self.current_song_info = None
            self.current_song = None
            self.is_playing = False

    def get_search_results(self, search_term):
        return self.get_vid_list(search_term)

    def get_vid_list(self, search):
        url = "https://www.youtube.com/results?search_query=" + search.replace(" ", "+")
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        all_searches = soup.findAll(attrs={'class': 'yt-uix-tile-link'})
        search_results_list = []

        for i in range(10):
            search_dict = {"title": all_searches[i]['title'], 'href': all_searches[i]['href']}
            search_results_list.append(search_dict)

        return search_results_list

    def get_choices(self, all_searches):
        list_urls = "<br>"
        for i in range(10):
            completed_url = "https://www.youtube.com" + all_searches[i]['href']
            list_urls += f"<font color='yellow'>[{i}]:</font> <a href='{completed_url}'>[{all_searches[i]['title']}]</a><br>"
        return list_urls

    def clear_queue(self):
        self.queue_instance.clear()

    def download_song_name(self, url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            if info_dict['duration'] >= self.max_track_duration:
                return None
            if info_dict['duration'] <= 0.1:
                return None

            prep_struct = {
                    'main_id': info_dict['url'],
                    'main_title': info_dict['title'],
            }
            return prep_struct

    def play_audio(self, mumble):
        self.current_song_info = self.queue_instance.pop()
        self.current_song = self.current_song_info.get('main_id')

        stripped_url = BeautifulSoup(self.current_song, features='html.parser').get_text()
        uri = stripped_url

        command = utils.get_vlc_dir()
        mumble.sound_output.clear_buffer()

        if self.music_thread:
            self.music_thread.terminate()
            self.music_thread.kill()
            self.music_thread = None

        if self.music_thread is None:
            self.music_thread = sp.Popen([command, uri] + ['-I', 'dummy', '--quiet', '--no-repeat', '--sout',
                                                           '#transcode{acodec=s16le, channels=2, '
                                                           'samplerate=24000, ab=192, threads=8}:std{access=file, '
                                                           'mux=wav, dst=-}'],
                                         stdout=sp.PIPE, bufsize=480)

        self.is_playing = True
        utils.unmute(mumble)
        utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                   f"Now playing: {self.current_song_info['main_title']}")

        while not self.exit_flag and mumble.isAlive():
            while mumble.sound_output.get_buffer_size() > 0.5 and not self.exit_flag:
                time.sleep(0.01)
            if self.music_thread:
                raw_music = self.music_thread.stdout.read(480)
                if raw_music and self.music_thread and self.is_playing:  # raw_music and
                    mumble.sound_output.add_sound(audioop.mul(raw_music, 2, self.volume))
                else:
                    time.sleep(0.1)
            else:
                time.sleep(0.1)
        return

    def audio_loop(self, mumble):
        if not self.is_playing:
            while not self.queue_instance.is_empty() and mumble.isAlive():
                self.play_audio(mumble)

    def get_queue(self):
        if self.queue_instance.size() is 0:
            return None
        queue_titles = "<font color='red'>Youtube Queue:</font><br>"
        queue_list = list(self.queue_instance.queue_storage)
        counter = 0
        for i in range(len(queue_list)-1, -1, -1):
            queue_titles += f"<font color='cyan'>[{counter}]: </font><font color='yellow'>{queue_list[i]['main_title']}</font><br>"
            counter += 1
        return queue_titles

    def plugin_test(self):
        debug_print("Youtube Plugin self-test callback.")

    def quit(self):
        self.stop_audio()
        self.exit_flag = True
        debug_print("Exiting Youtube Plugin...")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
