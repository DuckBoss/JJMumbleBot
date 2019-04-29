import os
import utils
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print
import urllib.request
from bs4 import BeautifulSoup
import youtube_dl
import subprocess as sp
import time
import audioop
import threading


class YoutubeHelper:
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True,
        'logger': GM.logger,
        'outtmpl': f'{utils.get_temporary_img_dir()}%(id)s.jpg',
        'skip_download': True,
        'writethumbnail': True
    }
    exit_flag = False
    queue_instance = None
    all_searches = None
    can_play = False
    is_playing = False
    current_song = None
    current_song_info = None
    music_thread = None
    # Autoplay enabled/disabled
    autoplay = True
    # default volume
    volume = 0.5
    # max number of tracks in the queue.
    max_queue_size = 25
    # max track duration in seconds.
    max_track_duration = 900


def get_queue():
    if YoutubeHelper.queue_instance.size() is 0:
        return None
    list_queue = [f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Youtube Queue:</font>"]
    queue_list = list(YoutubeHelper.queue_instance.queue_storage)
    counter = 0
    for i in range(len(queue_list) - 1, -1, -1):
        list_queue.append(f"<br><font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>[{counter}]</font> - {queue_list[i]['main_title']}")
        counter += 1
    return list_queue


def next():
    if YoutubeHelper.music_thread is not None:
        if YoutubeHelper.queue_instance.is_empty():
            GM.gui.quick_gui(
                "The youtube queue is empty, so I can't go to the next song.",
                text_type='header',
                box_align='left')
            return
        GM.gui.quick_gui(
            "Going to next available track.",
            text_type='header',
            box_align='left')
        GM.logger.info("The youtube audio queue moved to the next available track.")
        stop_audio()
        # doesn't need a 'download_next()' here because the next song thumbnail should already be downloaded.
        play_audio()
        return
    return


def skipto(skip_val):
    if YoutubeHelper.music_thread is not None:
        if YoutubeHelper.queue_instance.is_empty():
            GM.gui.quick_gui(
                "The youtube queue is empty, so I can't skip tracks.",
                text_type='header',
                box_align='left')
            return
        if skip_val > YoutubeHelper.queue_instance.size() - 1:
            GM.gui.quick_gui(
                f"You can't skip beyond the length of the current queue.",
                text_type='header',
                box_align='left')
            return
        if skip_val < 1:
            next()
            return
        GM.gui.quick_gui(
            f"Skipping to track {skip_val} in the queue.",
            text_type='header',
            box_align='left')
        for i in range(skip_val):
            YoutubeHelper.queue_instance.pop()

        GM.logger.info("The youtube audio queue skipped tracks.")
        stop_audio()
        download_next()
        play_audio()
        return


def download_song_name(url):
    try:
        with youtube_dl.YoutubeDL(YoutubeHelper.ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=True)
            if info_dict['duration'] >= YoutubeHelper.max_track_duration:
                return None
            if info_dict['duration'] <= 0.1:
                return None

            prep_struct = {
                'main_url': info_dict['url'],
                'main_title': info_dict['title'],
                'img_id': info_dict['id']
            }
            return prep_struct
    except youtube_dl.utils.DownloadError:
        return None


def clear_queue():
    YoutubeHelper.queue_instance.clear()
    utils.clear_directory(utils.get_temporary_img_dir())


def download_next():
    queue_list = list(YoutubeHelper.queue_instance.queue_storage)
    # print(queue_list)
    youtube_url = None
    if len(queue_list) > 0:
        youtube_url = queue_list[-1]['main_url']
    else:
        return
    if os.path.isfile(utils.get_temporary_img_dir() + f"{queue_list[-1]['img_id']}.jpg"):
        # print("Thumbnail exists...skipping")
        return
    try:
        with youtube_dl.YoutubeDL(YoutubeHelper.ydl_opts) as ydl:
            ydl.extract_info(youtube_url, download=True)
            #if video['duration'] >= YoutubeHelper.max_track_duration or video['duration'] <= 0.1:
            #    debug_print("Video length exceeds limit...skipping.")
            #    YoutubeHelper.queue_instance.pop()
    except youtube_dl.utils.DownloadError:
        return
    return


def download_specific(index):
    queue_list = list(YoutubeHelper.queue_instance.queue_storage)
    youtube_url = None
    if len(queue_list) > 0:
        youtube_url = queue_list[index]['main_url']
    else:
        return
    if os.path.isfile(utils.get_temporary_img_dir() + f"{queue_list[index]['img_id']}.jpg"):
        return
    try:
        with youtube_dl.YoutubeDL(YoutubeHelper.ydl_opts) as ydl:
            ydl.extract_info(youtube_url, download=True)
    except youtube_dl.utils.DownloadError:
        return
    return


def download_playlist(url):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': False,
        'extract_flat': True,
        'logger': GM.logger,
        'outtmpl': f'{utils.get_temporary_img_dir()}%(id)s.jpg',
        'skip_download': True,
        'writethumbnail': True,
        'ignoreerrors': True
    }
    if GM.cfg.getboolean('Plugin_Settings', 'Youtube_AllowPlaylistMax'):
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'noplaylist': False,
            'extract_flat': True,
            'logger': GM.logger,
            'outtmpl': f'{utils.get_temporary_img_dir()}%(id)s.jpg',
            'skip_download': True,
            'writethumbnail': True,
            'ignoreerrors': True,
            'playlistend': int(GM.cfg['Plugin_Settings']['Youtube_MaxPlaylistLength'])
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        playlist_dict_check = ydl.extract_info(url, download=False, process=False)
        if playlist_dict_check is None:
            GM.gui.quick_gui(
                f"ERROR: This playlist is private. Only unlisted/public playlists can be played.",
                text_type='header',
                box_align='left')
            return None
        if 'entries' in playlist_dict_check:
            count = 0
            for entry in playlist_dict_check['entries']:
                count += 1
            # print(f"Playlist length: {count}")
            if count > int(GM.cfg['Plugin_Settings']['Youtube_MaxPlaylistLength']):
                if not GM.cfg.getboolean('Plugin_Settings', 'Youtube_AllowPlaylistMax'):
                    GM.gui.quick_gui(
                        f"ERROR: This playlist is longer than the limit set in the config.<br>The current limit is {GM.cfg['Plugin_Settings']['Youtube_MaxPlaylistLength']}.",
                        text_type='header',
                        box_align='left')
                    return None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        GM.gui.quick_gui(
            "The playlist is being generated...",
            text_type='header',
            box_align='left')
        playlist_dict = ydl.extract_info(url, download=True)
        all_videos = []
        if not playlist_dict['entries']:
            GM.gui.quick_gui(
                "ERROR: Unable to get playlist information.",
                text_type='header',
                box_align='left')
            return None
        for video in playlist_dict['entries']:
            if not video:
                debug_print("Unable to get video information...skipping.")
                continue
            # print(video)
            prep_struct = {
                'main_url': f"https://www.youtube.com/watch?v={video['id']}",
                'main_title': video['title'],
                'img_id': video['id']
            }
            all_videos.append(prep_struct)
        return all_videos


def clear_audio_thread():
    if YoutubeHelper.music_thread is not None:
        debug_print("Stopping audio thread.")
        YoutubeHelper.music_thread.terminate()
        YoutubeHelper.music_thread.kill()
        YoutubeHelper.music_thread = None
        YoutubeHelper.is_playing = False


def stop_current():
    if YoutubeHelper.music_thread is not None:
        YoutubeHelper.current_song_info = None
        YoutubeHelper.current_song = None
        YoutubeHelper.is_playing = False


def stop_audio():
    if YoutubeHelper.music_thread is not None:
        debug_print("Stopping audio thread.")
        YoutubeHelper.music_thread.terminate()
        YoutubeHelper.music_thread.kill()
        YoutubeHelper.music_thread = None
        YoutubeHelper.current_song_info = None
        YoutubeHelper.current_song = None
        YoutubeHelper.is_playing = False


def get_search_results(search_term):
    return get_vid_list(search_term)


def get_vid_list(search):
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


def get_choices(all_searches):
    list_urls = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Search Results:</font><br>"
    for i in range(10):
        completed_url = "https://www.youtube.com" + all_searches[i]['href']
        list_urls += f"<font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>[{i}]</font> - <a href='{completed_url}'>[{all_searches[i]['title']}]</a><br>"
    return list_urls


def play_audio():
    GM.mumble.sound_output.clear_buffer()
    time.sleep(0.1)

    YoutubeHelper.current_song_info = YoutubeHelper.queue_instance.pop()
    if YoutubeHelper.current_song_info is None:
        stop_audio()
        return
    if YoutubeHelper.current_song_info['img_id'] is None:
        return
    YoutubeHelper.current_song = YoutubeHelper.current_song_info.get('main_url')

    stripped_url = BeautifulSoup(YoutubeHelper.current_song, features='html.parser').get_text()
    uri = stripped_url

    command = utils.get_vlc_dir()

    thr = None
    if not YoutubeHelper.queue_instance.is_empty():
        thr = threading.Thread(target=download_next)
        thr.start()

    #if YoutubeHelper.music_thread:
    #    YoutubeHelper.music_thread.terminate()
    #    YoutubeHelper.music_thread.kill()
    #    YoutubeHelper.music_thread = None

    #if YoutubeHelper.music_thread is None:
    YoutubeHelper.music_thread = sp.Popen(
        [command, uri] + ['-I', 'dummy', '--quiet', '--one-instance', '--no-repeat', '--sout',
                          '#transcode{acodec=s16le, channels=2, '
                          'samplerate=24000, ab=192, threads=8}:std{access=file, '
                          'mux=wav, dst=-}',
                          'vlc://quit'],
        stdout=sp.PIPE, bufsize=480)
        # YoutubeHelper.music_thread.wait()
    YoutubeHelper.is_playing = True
    utils.unmute()

    GM.gui.quick_gui_img(f"{utils.get_temporary_img_dir()}",
                         f"{YoutubeHelper.current_song_info['img_id']}",
                         caption=f"Now playing: {YoutubeHelper.current_song_info['main_title']}",
                         format=True,
                         img_size=32768)

    while not YoutubeHelper.exit_flag and GM.mumble.isAlive():
        while GM.mumble.sound_output.get_buffer_size() > 0.5 and not YoutubeHelper.exit_flag:
            time.sleep(0.01)
        if YoutubeHelper.music_thread:
            raw_music = YoutubeHelper.music_thread.stdout.read(480)
            if raw_music and YoutubeHelper.music_thread and YoutubeHelper.is_playing:
                GM.mumble.sound_output.add_sound(audioop.mul(raw_music, 2, YoutubeHelper.volume))
            else:
                if not YoutubeHelper.autoplay:
                    #time.sleep(0.1)
                    YoutubeHelper.is_playing = False
                    if thr:
                        thr.join()
                    return
                else:
                    YoutubeHelper.is_playing = False
                    if thr:
                        thr.join()
                    play_audio()
                    return
        else:
            return
    return


def set_max_track_duration(new_max):
    GM.max_track_duration = new_max
