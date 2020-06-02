from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils.print_utils import dprint, rprint
from JJMumbleBot.plugins.extensions.youtube.resources.strings import *
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import runtime_utils
import urllib.request
from bs4 import BeautifulSoup
import os
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
        'logger': GS.log_service,
        'outtmpl': f'{dir_utils.get_temp_med_dir()}/youtube/%(id)s.jpg',
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
    yt_metadata = None
    # Autoplay enabled/disabled
    autoplay = True
    # default volume
    volume = 0.5
    # max number of tracks in the queue.
    max_queue_size = 25
    # max track duration in seconds.
    max_track_duration = 900


def get_queue():
    if YoutubeHelper.queue_instance.size() == 0:
        return None
    list_queue = [f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Youtube Queue:</font>"]
    queue_list = list(YoutubeHelper.queue_instance.queue_storage)
    counter = 0
    for i in range(len(queue_list) - 1, -1, -1):
        list_queue.append(
            f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{counter}]</font> - {queue_list[i]['main_title']}")
        counter += 1
    return list_queue


def next_track():
    if GS.audio_inst is not None:
        if YoutubeHelper.queue_instance.is_empty():
            GS.gui_service.quick_gui(
                "The youtube queue is empty, so I can't go to the next song.",
                text_type='header',
                box_align='left')
            return
        GS.gui_service.quick_gui(
            "Going to next available track.",
            text_type='header',
            box_align='left')
        GS.log_service.info("The youtube audio queue moved to the next available track.")
        try:
            dir_utils.remove_file(f"{YoutubeHelper.current_song_info['img_id']}.jpg", f'{dir_utils.get_temp_med_dir()}/youtube')
        except FileNotFoundError:
            pass
        stop_audio()
        GS.audio_dni = (True, YoutubeHelper.yt_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        download_next()
        play_audio()
        return
    return


def skipto(skip_val):
    if GS.audio_inst is not None:
        if not GS.audio_dni[0]:
            GS.audio_dni = (True, YoutubeHelper.yt_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            if GS.audio_dni[1] != YoutubeHelper.yt_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]:
                rprint(
                    f'An audio plugin is using the audio thread with no interruption mode enabled. [{GS.audio_dni[1]}]')
                GS.gui_service.quick_gui(
                    "An audio plugin is using the audio thread with no interruption mode enabled.",
                    text_type='header',
                    box_align='left')
                return
        if YoutubeHelper.queue_instance.is_empty():
            GS.gui_service.quick_gui(
                "The youtube queue is empty, so I can't skip tracks.",
                text_type='header',
                box_align='left')
            return
        if skip_val > YoutubeHelper.queue_instance.size() - 1:
            GS.gui_service.quick_gui(
                f"You can't skip beyond the length of the current queue.",
                text_type='header',
                box_align='left')
            return
        if skip_val < 1:
            next_track()
            return
        GS.gui_service.quick_gui(
            f"Skipping to track {skip_val} in the queue.",
            text_type='header',
            box_align='left')
        for i in range(skip_val):
            YoutubeHelper.queue_instance.pop()

        GS.log_service.info("The youtube audio queue skipped tracks.")
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/youtube')
        stop_audio()
        GS.audio_dni = (True, YoutubeHelper.yt_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
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
    if not YoutubeHelper.is_playing:
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/youtube')


def download_next():
    queue_list = list(YoutubeHelper.queue_instance.queue_storage)
    # print(queue_list)
    youtube_url = None
    if len(queue_list) > 0:
        youtube_url = queue_list[-1]['main_url']
    else:
        return
    if os.path.isfile(f"{dir_utils.get_temp_med_dir()}/youtube/{queue_list[-1]['img_id']}.jpg"):
        # print("Thumbnail exists...skipping")
        return
    try:
        with youtube_dl.YoutubeDL(YoutubeHelper.ydl_opts) as ydl:
            ydl.extract_info(youtube_url, download=True)
            # if video['duration'] >= YoutubeHelper.max_track_duration or video['duration'] <= 0.1:
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
    if os.path.isfile(f"{dir_utils.get_temp_med_dir()}/youtube/{queue_list[index]['img_id']}.jpg"):
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
        'logger': GS.log_service,
        'outtmpl': f'{dir_utils.get_temp_med_dir()}/youtube/%(id)s.jpg',
        'skip_download': True,
        'writethumbnail': True,
        'ignoreerrors': True
    }
    if YoutubeHelper.yt_metadata.getboolean(C_PLUGIN_SETTINGS, P_YT_ALL_PLAY_MAX, fallback=True):
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'noplaylist': False,
            'extract_flat': True,
            'logger': GS.log_service,
            'outtmpl': f'{dir_utils.get_temp_med_dir()}/youtube/%(id)s.jpg',
            'skip_download': True,
            'writethumbnail': True,
            'ignoreerrors': True,
            'playlistend': int(YoutubeHelper.yt_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN])
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.cache.remove()
        playlist_dict_check = ydl.extract_info(url, download=False, process=False)
        if playlist_dict_check is None:
            GS.gui_service.quick_gui(
                f"ERROR: This playlist is private. Only unlisted/public playlists can be played.",
                text_type='header',
                box_align='left')
            return None
        if 'entries' in playlist_dict_check:
            count = 0
            for entry in playlist_dict_check['entries']:
                count += 1
            # print(f"Playlist length: {count}")
            if count > int(YoutubeHelper.yt_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN]):
                if not YoutubeHelper.yt_metadata.getboolean(C_PLUGIN_SETTINGS, P_YT_ALL_PLAY_MAX, fallback=True):
                    GS.gui_service.quick_gui(
                        f"ERROR: This playlist is longer than the limit set in the config.<br>The current limit is {YoutubeHelper.yt_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN]}.",
                        text_type='header',
                        box_align='left')
                    return None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        GS.gui_service.quick_gui(
            "The playlist is being generated...",
            text_type='header',
            box_align='left')
        playlist_dict = ydl.extract_info(url, download=True)
        all_videos = []
        if not playlist_dict['entries']:
            GS.gui_service.quick_gui(
                "ERROR: Unable to get playlist information.",
                text_type='header',
                box_align='left')
            return None
        for video in playlist_dict['entries']:
            if not video:
                dprint("Unable to get video information...skipping.")
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
    if GS.audio_inst is not None:
        dprint("Stopping audio thread.")
        GS.audio_inst.terminate()
        GS.audio_inst.kill()
        GS.audio_inst = None
        YoutubeHelper.is_playing = False
        GS.audio_dni = (False, None)


def stop_current():
    if GS.audio_inst is not None:
        YoutubeHelper.current_song_info = None
        YoutubeHelper.current_song = None
        YoutubeHelper.is_playing = False


def stop_audio():
    if GS.audio_inst is not None:
        dprint("Stopping audio thread.")
        GS.audio_inst.terminate()
        GS.audio_inst.kill()
        GS.audio_inst = None
        YoutubeHelper.current_song_info = None
        YoutubeHelper.current_song = None
        YoutubeHelper.is_playing = False
        GS.audio_dni = (False, None)


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
    list_urls = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Search Results:</font><br>"
    for i in range(10):
        completed_url = "https://www.youtube.com" + all_searches[i]['href']
        list_urls += f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - <a href='{completed_url}'>[{all_searches[i]['title']}]</a><br>"
    return list_urls


def play_audio():
    GS.audio_dni = (True, YoutubeHelper.yt_metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
    GS.mumble_inst.sound_output.clear_buffer()
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
    dprint(uri)
    dprint(YoutubeHelper.current_song)

    command = YoutubeHelper.yt_metadata[C_PLUGIN_SETTINGS][P_YT_VLC_DIR]

    thr = None
    if not YoutubeHelper.queue_instance.is_empty():
        thr = threading.Thread(target=download_next)
        thr.start()

    if GS.audio_inst:
        GS.audio_inst.terminate()
        GS.audio_inst.kill()
        GS.audio_inst = None

    if GS.audio_inst is None:
        use_stereo = GS.cfg.getboolean(C_MAIN_SETTINGS, P_AUD_STEREO)
        print(f"USE STEREO: {use_stereo}")
        if use_stereo:
            GS.audio_inst = sp.Popen(
                [command, uri] + ['-I', 'dummy', '--one-instance', '--no-repeat', '--sout',
                                  '#transcode{acodec=s16le, channels=2, '
                                  'samplerate=48000, ab=192, threads=8}:std{access=file, '
                                  'mux=wav, dst=-}',
                                  'vlc://quit'],
                stdout=sp.PIPE, bufsize=1024)
        else:
            GS.audio_inst = sp.Popen(
                [command, uri] + ['-I', 'dummy', '--one-instance', '--no-repeat', '--sout',
                                  '#transcode{acodec=s16le, channels=2, '
                                  'samplerate=24000, ab=192, threads=8}:std{access=file, '
                                  'mux=wav, dst=-}',
                                  'vlc://quit'],
                stdout=sp.PIPE, bufsize=1024)
    # YoutubeHelper.music_thread.wait()
    YoutubeHelper.is_playing = True
    runtime_utils.unmute()

    GS.gui_service.quick_gui_img(f"{dir_utils.get_temp_med_dir()}/youtube",
                                 f"{YoutubeHelper.current_song_info['img_id']}",
                                 caption=f"Now playing: {YoutubeHelper.current_song_info['main_title']}",
                                 format=True,
                                 img_size=32768)

    while not YoutubeHelper.exit_flag and GS.mumble_inst.isAlive():
        while GS.mumble_inst.sound_output.get_buffer_size() > 0.5 and not YoutubeHelper.exit_flag:
            time.sleep(0.01)
        if GS.audio_inst:
            raw_music = GS.audio_inst.stdout.read(1024)
            if raw_music and GS.audio_inst and YoutubeHelper.is_playing:
                GS.mumble_inst.sound_output.add_sound(audioop.mul(raw_music, 2, YoutubeHelper.volume))
            else:
                if not YoutubeHelper.autoplay:
                    YoutubeHelper.is_playing = False
                    if thr:
                        thr.join()
                    try:
                        dir_utils.remove_file(f"{YoutubeHelper.current_song_info['img_id']}.jpg",
                                              f'{dir_utils.get_temp_med_dir()}/youtube')
                        if YoutubeHelper.queue_instance.size() < 1:
                            dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/youtube')
                    except (FileNotFoundError, TypeError):
                        pass
                    download_next()
                    return
                YoutubeHelper.is_playing = False
                if thr:
                    thr.join()
                try:
                    dir_utils.remove_file(f"{YoutubeHelper.current_song_info['img_id']}.jpg",
                                          f'{dir_utils.get_temp_med_dir()}/youtube')
                    if YoutubeHelper.queue_instance.size() < 1:
                        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/youtube')
                except (FileNotFoundError, TypeError):
                    pass
                download_next()
                play_audio()
                return
        else:
            return
    return


def set_max_track_duration(new_max):
    GS.max_track_duration = new_max
