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


class Plugin(PluginBase):
    help_data = "<br><b><font color='red'>#####</font> Youtube Plugin Help <font color='red'>#####</font></b><br> \
                        All commands can be run by typing it in the channel or privately messaging DuckBot.<br>\
                        <b>!youtube/!yt 'search_term'</b>: Searches youtube for a song/video.<br>\
                        <b>!play/!p 'item_number' 'item_count'(optional)</b>: Plays the selected song from youtube.<br>\
                        <b>!stop</b>: Stops the currently playing track.<br>\
                        <b>!volume/!v '0..1'</b>: Sets the bot audio volume.<br>\
                        <b>!replay/!rp</b>: Replays the last played audio track.<br>\
                        <b>!next/!skip</b>: Goes to the next song in the queue.<br>\
                        <b>!queue/!q</b>: Displays the youtube queue.<br>\
                        <b>!song</b>: Shows currently playing track.<br>\
                        <b>!clear</b>: Clears the current youtube queue.<br>\
                        <b>!clear_cache</b>: Clears the youtube temporary media cache."

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': utils.get_temporary_media_dir()+'%(id)s.wav',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192', }]
    }

    queue_instance = None
    all_searches = None
    can_play = False
    is_playing = False
    current_song = None
    current_song_info = None
    music_thread = None
    exit_flag = False
    volume = 0.5

    sound_board_plugin = None

    max_queue_size = 25
    max_track_duration = 900

    def __init__(self, mumble):
        print("Music Plugin Initialized...")
        super().__init__()
        utils.clear_directory(utils.get_temporary_media_dir())
        self.queue_instance = qh.QueueHandler(self.max_queue_size)
        self.audio_loop(mumble)

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
            if self.current_song_info is not None:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Now playing: %s" % self.current_song_info['main_title'])
            else:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "DuckBot is not playing anything right now.")
            return

        elif command == "next" or command == "skip":
            if self.music_thread is not None:
                if self.queue_instance.is_empty():
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "The youtube queue is empty, so I can't go to the next song.")
                    return
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Going to next available track...")
                self.stop_audio()
                return
            return

        elif command == "stop":
            if self.music_thread is not None:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Stopping youtube audio thread...")
                self.queue_instance.clear()
                self.stop_audio()
                self.queue_instance = qh.QueueHandler(self.max_queue_size)
                return
            return

        elif command == "clear_cache":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            print("Clearing youtube temporary media cache.")
            self.clear_download_cache(mumble)
            return

        elif command == "clear":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            print("Clearing youtube queue.")
            self.clear_queue()
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Cleared youtube queue.")
            return

        elif command == "max_duration":
            if utils.privileges_check(mumble.users[text.actor]) != pv.Privileges.ADMIN:
                return
            try:
                new_max = int(message[1:].split(' ', 1)[1])
                self.set_max_track_duration(new_max)
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Set youtube track max duration to %s" % self.max_track_duration)
            except IndexError:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Current youtube track max duration: %s" % self.max_track_duration)
                return

        elif command == "volume" or command == "v":
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Current youtube volume: %s" % self.volume)
                return

            if vol > 1:
                self.volume = 1
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Invalid Volume Input: [0-1]")
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Set volume to %s" % self.volume)
                return
            if vol < 0:
                self.volume = 0
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Invalid Volume Input: [0-1]")
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Set volume to %s" % self.volume)
                return
            self.volume = vol
            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "Set volume to %s" % self.volume)
            return

        elif command == "youtube" or command == "yt":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            try:
                search_term = message_parse[1]
            except IndexError:
                return
            
            self.all_searches = self.get_search_results(search_term)
            search_results = self.get_choices(self.all_searches)

            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                       "%s\n%s" % (search_results, "Which one would you like to play? "))
            self.can_play = True
            return

        elif command == "queue" or command == "q":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            queue_results = self.get_queue()
            if queue_results is not None:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "<br>%s" % self.get_queue())
                return
            else:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "The youtube queue is empty.")
            return

        elif command == "play" or command == "p":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            if self.can_play:
                # self.sound_board_plugin.clear_audio_thread()
                # self.stop_audio()
                if self.queue_instance.is_full():
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "The youtube queue is full!")
                    return

                if len(all_messages) == 1:
                    utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "Automatically chosen: %s" % self.all_searches[0]['title'])
                    song_data = self.get_downloaded_song(
                        "https://www.youtube.com" + self.all_searches[0]['href'])
                    if song_data is None:
                        utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "The chosen video is too long. The maximum video length is %d minutes" % (self.max_track_duration/60))
                        return
                    self.can_play = False
                    self.queue_instance.insert(song_data)
                    self.audio_loop(mumble)
                    return
                elif len(all_messages) == 2:
                    if 9 >= int(all_messages[1]) >= 0:
                        utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                                   "You've chosen: %s" % (self.all_searches[int(all_messages[1])]['title']))
                        song_data = self.get_downloaded_song(
                            "https://www.youtube.com" + self.all_searches[int(all_messages[1])]['href'])
                        if song_data is None:
                            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "The chosen video is too long. The maximum video length is %d minutes" % (self.max_track_duration/60))
                            return
                        self.can_play = False
                    else:
                        utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "Invalid choice! Valid Range [0-9]")
                        self.can_play = False
                        return
                    self.queue_instance.insert(song_data)
                    self.audio_loop(mumble)
                elif len(all_messages) == 3:
                    if 9 >= int(all_messages[1]) >= 0:
                        utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                                   "You've chosen: %s" % (self.all_searches[int(all_messages[1])]['title']))
                        song_data = self.get_downloaded_song(
                            "https://www.youtube.com" + self.all_searches[int(all_messages[1])]['href'])
                        if song_data is None:
                            utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "The chosen video is too long. The maximum video length is %d minutes" % (self.max_track_duration/60))
                            return
                        self.can_play = False
                    else:
                        utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                               "Invalid choice! Valid Range [0-9]")
                        self.can_play = False
                        return
                    count = int(all_messages[2])
                    for i in range(count):
                        self.queue_instance.insert(song_data)
                    self.audio_loop(mumble)
                    return
            return

        elif command == "replay" or command == "rp":
            if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                return
            if self.music_thread is not None:
                if self.current_song is not None and self.current_song_info is not None:
                    if utils.privileges_check(mumble.users[text.actor]) == pv.Privileges.BLACKLIST:
                        return
                    self.queue_instance.insert_priority(self.current_song_info)
                    self.stop_audio()
            else:
                utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "There is no track available to replay.")
                return
            return

    def clear_audio_thread(self):
        if self.music_thread is not None:
            print("Stopping audio thread...")
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
            print("Stopping audio thread...")
            self.music_thread.terminate()
            self.music_thread.kill()
            self.music_thread = None
            self.current_song_info = None
            self.current_song = None
            self.is_playing = False

    def get_search_results(self, search_term):
        return self.get_vid_list(search_term)

    def get_downloaded_song(self, url):
        return self.download_song(url)

    def get_vid_list(self, search):
        url = "https://www.youtube.com/results?search_query=" + search.replace(" ", "+")
        response = urllib.request.urlopen(url)
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
            list_urls += "[%d]: <a href='%s'>[%s]</a><br>" % (i, completed_url, all_searches[i]['title'])
        return list_urls

    def clear_queue(self):
        self.queue_instance.clear()

    def clear_download_cache(self, mumble):
        self.stop_audio()
        time.sleep(1)
        utils.clear_directory(utils.get_temporary_media_dir())
        print("youtube temporary media cache cleared.")
        utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                           "Cleared youtube temporary media cache.")

    def download_song(self, url):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            if info_dict['duration'] >= self.max_track_duration:
                return None

            if os.path.isfile(utils.get_temporary_media_dir()+"%s.wav" % info_dict['id']):
                print("File exists, skipping download...")
                prep_struct = {
                    'main_id': info_dict['id'],
                    'main_title': info_dict['title'],
                }
                return prep_struct
            else:
                download_target = ydl.prepare_filename(info_dict)
                ydl.download([url])
                prep_struct = {
                    'main_id': info_dict['id'],
                    'main_title': info_dict['title'],
                }
                return prep_struct

    def play_audio(self, mumble):
        self.current_song_info = self.queue_instance.pop()
        self.current_song = self.current_song_info['main_id']

        uri = "file:///%s%s.wav" % (utils.get_temporary_media_dir(), self.current_song)
        command = utils.get_vlc_dir()
        mumble.sound_output.clear_buffer()

        if self.music_thread is None:
            self.music_thread = sp.Popen([command, uri] + ['-I', 'dummy', '--no-repeat', '--sout',
                                                           '#transcode{acodec=s16le, channels=2, '
                                                           'samplerate=24000, ab=192, threads=8}:std{access=file, '
                                                           'mux=wav, dst=-}'],
                                         stdout=sp.PIPE, bufsize=4096)

        self.is_playing = True
        utils.unmute(mumble)
        utils.echo(mumble.channels[mumble.users.myself['channel_id']],
                   "Now playing: <a href='%s'>%s</a>" % (
                       self.current_song_info['main_title'], self.current_song_info['main_title']))

        while not self.exit_flag and mumble.isAlive() and self.is_playing:
            while mumble.sound_output.get_buffer_size() > 0.5 and not self.exit_flag:
                time.sleep(0.01)
            if self.music_thread:
                raw_music = self.music_thread.stdout.read(4096)
                if raw_music and self.music_thread and self.is_playing:  # raw_music and
                    mumble.sound_output.add_sound(audioop.mul(raw_music, 2, self.volume))
                else:
                    time.sleep(0.1)
            else:
                time.sleep(0.1)

        while mumble.sound_output.get_buffer_size() > 0:
            time.sleep(0.01)

    def audio_loop(self, mumble):
        if not self.is_playing:
            while not self.queue_instance.is_empty():
                self.play_audio(mumble)

    def get_queue(self):
        if self.queue_instance.size() is 0:
            return None
        queue_titles = "<font color='red'>Youtube Queue:</font><br>"
        queue_list = list(self.queue_instance.queue_storage)
        counter = 0
        for i in range(len(queue_list)-1, -1, -1):
            queue_titles += "<font color='cyan'>[%d]: </font><font color='yellow'>%s</font><br>" % (counter, queue_list[i]['main_title'])
            counter += 1
        return queue_titles

    def plugin_test(self):
        print("Youtube Plugin self-test callback.")

    def quit(self):
        self.stop_audio()
        self.exit_flag = True
        print("Exiting Youtube Plugin...")

    def help(self):
        return self.help_data
