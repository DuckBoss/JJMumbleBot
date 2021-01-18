import youtube_dl
from PIL import Image
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.plugins.extensions.media.resources.strings import *
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.audio.audio_api import TrackType, TrackInfo
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import runtime_settings
from JJMumbleBot.plugins.extensions.media.utility import settings
from JJMumbleBot.plugins.extensions.media.utility.youtube_search import YoutubeSearch
import os
from zlib import crc32


def on_next_track():
    if gs.aud_interface.status.get_track().track_type == TrackType.STREAM:
        # If the track is looping, there is no need to download the next track image.
        if gs.aud_interface.status.is_looping():
            # Get new set of metadata for the current track if it is looping
            # because the link may expire and cause an issue.
            cur_track = gs.aud_interface.get_track()
            song_data = get_video_info(cur_track.alt_uri)
            if song_data is None:
                return
            track_obj = TrackInfo(
                uri=song_data['main_url'],
                name=cur_track.name,
                sender=cur_track.sender,
                duration=int(song_data['duration']),
                track_type=TrackType.STREAM,
                track_id=cur_track.track_id,
                alt_uri=cur_track.alt_uri,
                image_uri=cur_track.image_uri,
                quiet=False
            )
            gs.aud_interface.status.set_track(track_obj)
            return
        # If the queue is empty, there is no track image to download.
        if gs.aud_interface.status.get_queue_length() == 0:
            return

        download_thumbnail(gs.aud_interface.status.get_queue()[0])
        # Get the video metadata and fill in the information if the current track is missing metadata information.
        if gs.aud_interface.status.get_queue()[0].uri == '':
            if gs.aud_interface.status.get_queue()[0].alt_uri == '':
                return
            song_data = get_video_info(gs.aud_interface.status.get_queue()[0].alt_uri)
            if song_data is None:
                return
            track_obj = TrackInfo(
                uri=song_data['main_url'],
                name=gs.aud_interface.status.get_queue()[0].name,
                sender=gs.aud_interface.status.get_queue()[0].sender,
                duration=int(song_data["duration"]),
                track_type=TrackType.STREAM,
                track_id=gs.aud_interface.status.get_queue()[0].track_id,
                alt_uri=gs.aud_interface.status.get_queue()[0].alt_uri,
                image_uri=gs.aud_interface.status.get_queue()[0].image_uri,
                quiet=False
            )
            gs.aud_interface.status.set_track(track_obj)
            cur_track_hashed_img_uri = hex(crc32(str.encode(track_obj.track_id)) & 0xffffffff)
            gs.aud_interface.status["img_uri_hashed"] = cur_track_hashed_img_uri


def song_integrity_check():
    # Get the video metadata and fill in the information if the current track is missing metadata information.
    cur_track = gs.aud_interface.status.get_track()
    if cur_track.uri == '':
        if cur_track.alt_uri == '':
            return
        song_data = get_video_info(cur_track.alt_uri)
        if song_data is None:
            return
        track_obj = TrackInfo(
            uri=song_data['main_url'],
            name=cur_track.name,
            sender=cur_track.sender,
            duration=int(song_data['duration']),
            track_type=TrackType.STREAM,
            track_id=cur_track.track_id,
            alt_uri=cur_track.alt_uri,
            image_uri=cur_track.image_uri,
            quiet=False
        )
        gs.aud_interface.status.set_track(track_obj)
        cur_track_hashed_img_uri = hex(crc32(str.encode(track_obj.track_id)) & 0xffffffff)
        gs.aud_interface.status["img_uri_hashed"] = cur_track_hashed_img_uri


def on_play():
    if gs.aud_interface.status.get_track().track_type == TrackType.STREAM:
        cur_track = gs.aud_interface.get_track()
        download_thumbnail(cur_track)

        # Get the video metadata and fill in the information if the current track is missing metadata information.
        if cur_track.uri == '':
            if cur_track.alt_uri == '':
                return
            song_data = get_video_info(cur_track.alt_uri)
            if song_data is None:
                return
            track_obj = TrackInfo(
                uri=song_data['main_url'],
                name=cur_track.name,
                sender=cur_track.sender,
                duration=int(song_data['duration']),
                track_type=TrackType.STREAM,
                track_id=cur_track.track_id,
                alt_uri=cur_track.alt_uri,
                image_uri=cur_track.image_uri,
                quiet=False
            )
            gs.aud_interface.status.set_track(track_obj)
            cur_track_hashed_img_uri = hex(crc32(str.encode(track_obj.track_id)) & 0xffffffff)
            gs.aud_interface.status["img_uri_hashed"] = cur_track_hashed_img_uri


def on_skip():
    if gs.aud_interface.status.get_track().track_type == TrackType.STREAM:
        # Clear the thumbnails since the queue order has shifted.
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}')
        log(INFO, "Cleared the temporary media folder when skipping tracks.", origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)


def download_thumbnail(cur_track):
    cur_track_hashed_img_uri = hex(crc32(str.encode(cur_track.track_id)) & 0xffffffff)
    if os.path.exists(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track_hashed_img_uri}.jpg"):
        log(WARNING, f"Thumbnail exists for '{cur_track.name}'...skipping",
            origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
        return
    try:
        ydl_opts = {
            'quiet': True,
            'outtmpl': f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track_hashed_img_uri}.%(ext)s',
            'skip_download': True,
            'writethumbnail': True,
            'proxy': gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_PROXY_URL]
        }
        if runtime_settings.use_logging:
            ydl_opts['logger'] = gs.log_service
        if len(gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE]) > 0:
            ydl_opts['cookiefile'] = gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            ydl.extract_info(cur_track.alt_uri, download=True)
    except youtube_dl.utils.DownloadError as e:
        log(ERROR, f"Encountered a youtube_dl download error while retrieving the thumbnail for {cur_track.name}.\n{e}",
            origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
    # Patch youtube-dl sometimes providing webp instead of jpg (youtube-dl needs to fix this).
    if os.path.exists(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track_hashed_img_uri}.webp"):
        im = Image.open(
            f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track_hashed_img_uri}.webp").convert(
            "RGB")
        im.save(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track_hashed_img_uri}.jpg",
                "jpeg")
        os.remove(f"{dir_utils.get_temp_med_dir()}/{settings.plugin_name}/{cur_track_hashed_img_uri}.webp")
        log(WARNING, f"The retrieved thumbnail was in an invalid format and has been fixed for {cur_track.name}.",
            origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)


def on_stop():
    # Clear the thumbnails since the queue is cleared.
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}')
    log(INFO, "Cleared the thumbnails in the temporary media folder when stopping audio interface.", origin=L_GENERAL,
        print_mode=PrintMode.VERBOSE_PRINT.value)
    settings.can_play = False
    settings.search_results = None


def on_reset():
    # Clear the thumbnails since the queue is cleared.
    dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{settings.plugin_name}')
    log(INFO, "Cleared the thumbnails in the temporary media folder when resetting audio interface.", origin=L_GENERAL,
        print_mode=PrintMode.VERBOSE_PRINT.value)
    settings.can_play = False
    settings.search_results = None


def get_video_info(video_url):
    # Update the audio interface status with the media mrl, duration, and video title.
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'noplaylist': True,
            'skip_download': True,
            'proxy': gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_PROXY_URL]
        }
        if runtime_settings.use_logging:
            ydl_opts['logger'] = gs.log_service
        if len(gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE]) > 0:
            ydl_opts['cookiefile'] = gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE]

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
        log(ERROR, f"Encountered a youtube_dl download error while retrieving the video information for {video_url}.\n{e}",
            origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
        return None


def get_playlist_info(playlist_url):
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': False,
        'extract_flat': True,
        'skip_download': True,
        'writethumbnail': False,
        'ignoreerrors': True,
        'proxy': gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_PROXY_URL]
    }
    if runtime_settings.use_logging:
        ydl_opts['logger'] = gs.log_service
    if len(gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE]) > 0:
        ydl_opts['cookiefile'] = gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE]
    if settings.youtube_metadata.getboolean(C_PLUGIN_SETTINGS, P_YT_ALL_PLAY_MAX, fallback=True):
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'noplaylist': False,
            'extract_flat': True,
            'skip_download': True,
            'writethumbnail': False,
            'ignoreerrors': True,
            'proxy': gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_PROXY_URL],
            'playlistend': int(settings.youtube_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN])
        }
        if runtime_settings.use_logging:
            ydl_opts['logger'] = gs.log_service
        if len(gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE]) > 0:
            ydl_opts['cookiefile'] = gs.cfg[C_MEDIA_SETTINGS][P_MEDIA_COOKIE_FILE]
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        playlist_dict_check = ydl.extract_info(playlist_url, download=False, process=False)
        if playlist_dict_check is None:
            log(ERROR,
                f"The provided playlist cannot be played as it is either private or protected.",
                origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                f"This playlist is private or protected. Only unlisted/public playlists can be played.",
                text_type='header',
                box_align='left')
            return None
        playlist_dict_check['entries'] = list(playlist_dict_check['entries'])
        count = len(playlist_dict_check['entries'])
        if count > int(settings.youtube_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN]):
            if not settings.youtube_metadata.getboolean(C_PLUGIN_SETTINGS, P_YT_ALL_PLAY_MAX, fallback=True):
                log(ERROR,
                    [
                        "The provided playlist is longer than the limit set in the config.",
                        f"The current limit is {settings.youtube_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN]}."
                    ],
                    origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
                gs.gui_service.quick_gui(
                    [
                        "This playlist is longer than the limit set in the config.",
                        f"The current limit is {settings.youtube_metadata[C_PLUGIN_SETTINGS][P_YT_MAX_PLAY_LEN]}."
                    ],
                    text_type='header',
                    box_align='left')
                return None
        log(INFO,
            f"Generating playlist from the given url: {playlist_url}",
            origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
        gs.gui_service.quick_gui(
            "The playlist is being generated...this might take a while.",
            text_type='header',
            box_align='left')
        playlist_dict = ydl.extract_info(playlist_url, download=False, process=False)
        all_videos = []
        if not playlist_dict['entries']:
            log(ERROR,
                f"Unable to retrieve playlist information from the given url: {playlist_url}",
                origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                "Unable to get playlist information.",
                text_type='header',
                box_align='left')
            return None
        for video in list(playlist_dict['entries']):
            if not video:
                log(ERROR,
                    [
                        f"Unable to retrieve video information in the playlist from the given url: {playlist_url}",
                        "Skipping to the next video in the queue..."
                    ],
                    origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)
                continue
            prep_struct = {
                'std_url': f"https://www.youtube.com/watch?v={video['url']}",
                'main_url': '',
                'main_title': video['title'],
                'main_id': video['id'],
                'duration': '',
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
