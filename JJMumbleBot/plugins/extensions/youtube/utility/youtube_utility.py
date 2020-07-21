import youtube_dl
from PIL import Image
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.youtube.resources.strings import *
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.vlc.vlc_api import TrackType
from JJMumbleBot.lib.utils import print_utils
from JJMumbleBot.plugins.extensions.youtube.utility import settings
from JJMumbleBot.plugins.extensions.youtube.utility.youtube_search import YoutubeSearch
import os


def on_next_track():
    if gs.vlc_interface.status.get_track().track_type == TrackType.STREAM:
        # If the track is looping, there is no need to download the next track image.
        if gs.vlc_interface.status.is_looping():
            return
        # If the queue is empty, there is no track image to download.
        if gs.vlc_interface.status.get_queue_length() == 0:
            return

        # Get the first track in the queue.
        next_track = gs.vlc_interface.status.get_queue()[0]

        if os.path.exists(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{next_track.track_id}.jpg"):
            print_utils.dprint(f"Thumbnail exists for '{next_track.name}.jpg'...skipping")
            return
        try:
            ydl_opts = {
                'quiet': True,
                'logger': gs.log_service,
                'outtmpl': f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{next_track.track_id}.jpg',
                'skip_download': True,
                'writethumbnail': True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove()
                ydl.extract_info(next_track.alt_uri, download=True)
        except youtube_dl.utils.DownloadError as e:
            print_utils.dprint(e)
        # Patch youtube-dl sometimes providing webp instead of jpg (youtube-dl needs to fix this).
        if os.path.exists(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{next_track.track_id}.webp"):
            im = Image.open(
                f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{next_track.track_id}.webp").convert(
                "RGB")
            im.save(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{next_track.track_id}.jpg",
                    "jpeg")
            os.remove(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{next_track.track_id}.webp")
            print_utils.dprint(f"Fixed thumbnail for {next_track.track_id}")


def on_play():
    if gs.vlc_interface.status.get_track().track_type == TrackType.STREAM:
        cur_track = gs.vlc_interface.get_track()
        print(cur_track)

        if os.path.exists(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.jpg"):
            print_utils.dprint(f"Thumbnail exists for '{cur_track.name}.jpg'...skipping")
            return
        try:
            ydl_opts = {
                'quiet': True,
                'logger': gs.log_service,
                'outtmpl': f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.jpg',
                'skip_download': True,
                'writethumbnail': True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove()
                ydl.extract_info(cur_track.alt_uri, download=True)
        except youtube_dl.utils.DownloadError as e:
            print_utils.dprint(e)
        # Patch youtube-dl sometimes providing webp instead of jpg (youtube-dl needs to fix this).
        if os.path.exists(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.webp"):
            im = Image.open(
                f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.webp").convert(
                "RGB")
            im.save(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.jpg",
                    "jpeg")
            os.remove(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.webp")
            print_utils.dprint(f"Fixed thumbnail for {cur_track.track_id}")


def on_skip():
    if gs.vlc_interface.status.get_track().track_type == TrackType.STREAM:
        # Clear the thumbnails since the queue order has shifted.
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}')

        cur_track = gs.vlc_interface.get_track()

        if os.path.exists(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.jpg"):
            print_utils.dprint(f"Thumbnail exists for '{cur_track.name}.jpg'...skipping")
            return
        try:
            ydl_opts = {
                'quiet': True,
                'logger': gs.log_service,
                'outtmpl': f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.jpg',
                'skip_download': True,
                'writethumbnail': True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove()
                ydl.extract_info(cur_track.alt_uri, download=True)
        except youtube_dl.utils.DownloadError as e:
            print_utils.dprint(e)
        # Patch youtube-dl sometimes providing webp instead of jpg (youtube-dl needs to fix this).
        if os.path.exists(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.webp"):
            im = Image.open(
                f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.webp").convert(
                "RGB")
            im.save(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.jpg",
                    "jpeg")
            os.remove(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track.track_id}.webp")
            print_utils.dprint(f"Fixed thumbnail for {cur_track.track_id}")


def on_stop():
    # Clear the thumbnails since the queue is cleared.
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}')
    settings.can_play = False
    settings.search_results = None


def on_reset():
    # Clear the thumbnails since the queue is cleared.
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}')
    settings.can_play = False
    settings.search_results = None


def get_video_info(video_url):
    # Update the audio interface status with the youtube mrl, duration, and video title.
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'noplaylist': True,
            'logger': gs.log_service,
            'skip_download': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(video_url, download=False)
            prep_struct = {
                'std_url': video_url,
                'main_url': info_dict['url'],
                'main_title': info_dict['title'],
                'main_id': info_dict['id'],
                'duration': info_dict['duration']
            }
            return prep_struct
    except youtube_dl.utils.DownloadError as e:
        print_utils.dprint(e)
        return None


def get_playlist_info(playlist_url):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': False,
        'extract_flat': True,
        'logger': gs.log_service,
        'outtmpl': f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/%(id)s.jpg',
        'skip_download': True,
        'writethumbnail': False,
        'ignoreerrors': True
    }
    if settings.youtube_metadata.getboolean(C_PLUGIN_SETTINGS, P_YT_ALL_PLAY_MAX, fallback=True):
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'noplaylist': False,
            'extract_flat': True,
            'logger': gs.log_service,
            'outtmpl': f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/%(id)s.jpg',
            'skip_download': True,
            'writethumbnail': True,
            'ignoreerrors': True,
            'playlistend': int(settings.youtube_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN])
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_dict_check = ydl.extract_info(playlist_url, download=False, process=False)
        if playlist_dict_check is None:
            gs.gui_service.quick_gui(
                f"ERROR: This playlist is private or protected. Only unlisted/public playlists can be played.",
                text_type='header',
                box_align='left')
            return None
        count = 0
        for i, entry in enumerate(playlist_dict_check['entries']):
            count += 1
        if count > int(settings.youtube_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN]):
            if not settings.youtube_metadata.getboolean(C_PLUGIN_SETTINGS, P_YT_ALL_PLAY_MAX, fallback=True):
                gs.gui_service.quick_gui(
                    f"ERROR: This playlist is longer than the limit set in the config.<br>The current limit is {settings.youtube_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN]}.",
                    text_type='header',
                    box_align='left')
                return None

        gs.gui_service.quick_gui(
            "The playlist is being generated...this might take a while.",
            text_type='header',
            box_align='left')
        playlist_dict = ydl.extract_info(playlist_url, download=False)
        all_videos = []
        if not playlist_dict['entries']:
            gs.gui_service.quick_gui(
                "ERROR: Unable to get playlist information.",
                text_type='header',
                box_align='left')
            return None
        for video in playlist_dict['entries']:
            if not video:
                print_utils.dprint("Unable to get video information...skipping.")
                continue
            temp_song_data = get_video_info(f"https://www.youtube.com/watch?v={video['url']}")
            if temp_song_data is None:
                continue
            prep_struct = {
                'std_url': temp_song_data['std_url'],
                'main_url': temp_song_data['main_url'],
                'main_title': temp_song_data['main_title'],
                'main_id': temp_song_data['main_id'],
                'duration': temp_song_data['duration']
            }
            all_videos.append(prep_struct)
        return all_videos


def get_search_results(search_term, results_length):
    search_results_list = []
    search_results = YoutubeSearch(search_term, max_results=results_length).to_dict()
    settings.search_results = search_results
    for i in range(results_length):
        search_results_list.append(search_results[i])

    if len(search_results_list) == 0:
        list_urls = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>No youtube search results found for: [{search_term}].</font><br>"
        return list_urls
    list_urls = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Search Results:</font><br>"
    for i, item in enumerate(search_results_list):
        completed_url = f"https://youtube.com{item['href']}"
        list_urls += f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - <a href='{completed_url}'>[{item['title']}]</a><br>"
    return list_urls
