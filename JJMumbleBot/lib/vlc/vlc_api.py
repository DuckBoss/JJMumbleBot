from time import sleep, time
import wave
import os
from zlib import crc32
from JJMumbleBot.lib.utils.print_utils import dprint
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.helpers import queue_handler
from JJMumbleBot.lib.vlc import audio_interface
from datetime import timedelta
from enum import Enum
from threading import Thread


class TrackStatus(Enum):
    PLAYING = 'playing'
    PAUSED = 'paused'
    STOPPED = 'stopped'


class TrackType(Enum):
    FILE = 'file'
    STREAM = 'stream'


class TrackInfo:
    def __init__(self, uri: str, name: str, sender: str, duration=None, track_type=None, track_id='', alt_uri='',
                 image_uri='', quiet=False):
        self.uri = uri
        self.name = name
        self.sender = sender
        self.duration = duration
        self.track_type = track_type
        self.alt_uri = alt_uri
        self.image_uri = image_uri
        self.track_id = track_id
        self.quiet = quiet

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {'uri': self.uri, 'name': self.name, 'sender': self.sender, 'duration': self.duration,
                'track_type': self.track_type, 'track_id': self.track_id, 'alt_uri': self.alt_uri,
                'image_uri': self.image_uri, 'quiet': self.quiet}


class VLCInterface:
    class Status(dict):
        def __init__(self):
            super().__init__(
                {
                    'plugin_owner': '',
                    'plugin_name': '',
                    'sender': '',
                    'track': TrackInfo(uri='', name='', sender='', duration=-1, track_type=TrackType.FILE),
                    'track_uri': '',
                    'alt_uri': '',
                    'image_uri': '',
                    'track_id': '',
                    'queue': [],
                    'queue_length': 0,
                    'status': TrackStatus.STOPPED,
                    'volume': float(global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_DEFAULT_VOLUME]),
                    'loop': False,
                    'duck_audio': global_settings.cfg.getboolean(C_MEDIA_SETTINGS, P_MEDIA_VLC_DUCK, fallback=False),
                    'ducking_volume': float(global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_DUCK_VOLUME]),
                    'ducking_threshold': float(global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_DUCK_THRESHOLD]),
                    'ducking_delay': float(global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_DUCK_DELAY]),
                    # Internal Audio Ducking Settings
                    'is_ducking': False,
                    'duck_start': 0.0,
                    'duck_end': 0.0,
                    'last_volume': float(global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_DEFAULT_VOLUME]),
                    'start_time': 0,
                    'pause_time': 0,
                    'progress_time': 0
                }
            )

        def __str__(self):
            dict_str = f"plugin_owner: {self['plugin_owner']}<br>" \
                       f"plugin_name: {self['plugin_name']}<br>" \
                       f"sender: {self['track'].sender}<br>" \
                       f"track: {self['track'].name}<br>" \
                       f"track_uri: {(self['track'].uri[:25] + (self['track'].uri[25:] and '...')) if len(self['track'].uri) > 0 else self['track'].uri}<br>" \
                       f"alt_uri: {(self['track'].alt_uri[:25] + (self['track'].alt_uri[25:] and '...')) if len(self['track'].alt_uri) > 0 else self['track'].alt_uri}<br>" \
                       f"image_uri: {(self['track'].image_uri[:25] + (self['track'].image_uri[25:] and '...')) if len(self['track'].image_uri) > 0 else self['track'].image_uri}<br>" \
                       f"track_id: {self['track'].track_id}<br>" \
                       f"quiet: {self['track'].quiet}<br>" \
                       f"duration: {self['track'].duration}<br>" \
                       f"type: {self['track'].track_type.value}<br>" \
                       f"queue: ["
            dict_str += ', '.join(x.name for x in self['queue'])
            dict_str += f"]<br>queue_length: {self['queue_length']}<br>" \
                        f"status: {self['status'].value}<br>" \
                        f"start_time: {self['start_time']}<br>" \
                        f"pause_time: {self['pause_time']}<br>" \
                        f"progress_time: {self['progress_time']}<br>" \
                        f"volume: {self.get_volume()}<br>" \
                        f"loop: {self['loop']}<br>" \
                        f"duck_audio: {self['duck_audio']}<br>" \
                        f"ducking_volume: {self['ducking_volume']}<br>" \
                        f"ducking_threshold: {self['ducking_threshold']}<br>" \
                        f"ducking_delay: {self['ducking_delay']}"
            return dict_str

        # Plugin owner
        def get_plugin_owner(self):
            return self.get('plugin_owner')

        def set_plugin_owner(self, owner_name):
            self['plugin_owner'] = owner_name

        def clear_plugin_owner(self):
            self['plugin_owner'] = ''

        # Track
        def get_track(self):
            return self.get('track', TrackInfo('', '', '', None, TrackType.FILE))

        def set_track(self, track_obj: TrackInfo):
            self['track'] = track_obj

        def clear_track(self):
            self['track'] = TrackInfo('', '', '', None, TrackType.FILE)

        def get_queue(self):
            return self['queue']

        def clear_queue(self):
            self['queue'] = []
            self['queue_length'] = 0

        def update_queue(self, queue):
            self['queue'] = queue
            self['queue_length'] = len(queue)

        def get_queue_length(self):
            return self['queue_length']

        # Volume
        def set_volume(self, volume):
            self['volume'] = volume

        def get_volume(self):
            return float(f"{self['volume']:.2f}")

        # Loop
        def enable_loop(self):
            self['loop'] = True

        def disable_loop(self):
            self['loop'] = False

        def is_looping(self):
            return self['loop']

        # Playing status
        def set_status(self, status: TrackStatus):
            self['status'] = status

        def get_status(self):
            return self['status']

        def is_playing(self):
            return True if self['status'] == TrackStatus.PLAYING else False

        def is_paused(self):
            return True if self['status'] == TrackStatus.PAUSED else False

        def is_stopped(self):
            return True if self['status'] == TrackStatus.STOPPED else False

    class AudioUtilites:
        def __init__(self):
            pass

        def sec_formatted(self, duration):
            return str(timedelta(seconds=int(duration)))

        def lerp_volume(self, cur_vol, targ_vol, lerp_time):
            cur_time = 0
            while cur_time < 1:
                global_settings.vlc_interface.status.set_volume(cur_vol + cur_time * (targ_vol - cur_vol))
                cur_time += lerp_time
                sleep(0.01)
            global_settings.vlc_interface.status.set_volume(targ_vol)

        def set_volume(self, volume: float, auto=False):
            if not auto:
                global_settings.vlc_interface.status['last_volume'] = volume
            lerp_thr = Thread(target=self.lerp_volume,
                              args=(float(global_settings.vlc_interface.status.get_volume()), volume, 0.025),
                              daemon=True)
            lerp_thr.start()

        def set_volume_fast(self, volume: float, auto=False):
            if not auto:
                global_settings.vlc_interface.status['last_volume'] = volume
            global_settings.vlc_interface.status.set_volume(volume)

        def set_last_volume(self, volume: float):
            global_settings.vlc_interface.status['last_volume'] = volume

        def duck_volume(self):
            if not self.is_ducking():
                global_settings.vlc_interface.status['is_ducking'] = True
                self.set_volume(global_settings.vlc_interface.status['ducking_volume'], auto=True)

        def set_duck_volume(self, volume: float):
            global_settings.vlc_interface.status['ducking_volume'] = volume

        def get_ducking_volume(self):
            return global_settings.vlc_interface.status['ducking_volume']

        def set_duck_threshold(self, threshold: float):
            if threshold < 0:
                return
            global_settings.vlc_interface.status['ducking_threshold'] = threshold

        def set_ducking_delay(self, delay: float):
            if delay < 0 or delay > 5:
                return
            global_settings.vlc_interface.status['ducking_delay'] = delay

        def get_ducking_threshold(self):
            return global_settings.vlc_interface.status['ducking_threshold']

        def get_ducking_delay(self):
            return global_settings.vlc_interface.status['ducking_delay']

        def unduck_volume(self):
            if self.is_ducking():
                self.set_volume(global_settings.vlc_interface.status['last_volume'], auto=True)
                global_settings.vlc_interface.status['duck_start'] = 0.0
                global_settings.vlc_interface.status['duck_end'] = 0.0
                global_settings.vlc_interface.status['is_ducking'] = False

        def is_ducking(self):
            return global_settings.vlc_interface.status['is_ducking']

        def can_duck(self):
            return global_settings.vlc_interface.status['duck_audio']

        def toggle_ducking(self):
            global_settings.vlc_interface.status['duck_audio'] = not global_settings.vlc_interface.status['duck_audio']

    def __init__(self):
        self.status = VLCInterface.Status()
        self.queue = queue_handler.QueueHandler([], maxlen=int(
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_QUEUE_LEN]))
        self.audio_utilities = VLCInterface.AudioUtilites()
        self.exit_flag: bool = False

    def callback_check(self, method_name):
        # Execute any callbacks subscribed to next_track
        for clbk in global_settings.plugin_callbacks:
            split_clbk = clbk.split('|')
            if split_clbk[0] == self.status['plugin_name'] and split_clbk[1] == method_name:
                global_settings.plugin_callbacks[clbk]()

    def play(self, override=False):
        if not override:
            if self.status.get_status() == TrackStatus.PLAYING:
                return
            if self.status.get_status() == TrackStatus.PAUSED:
                track_info = self.status.get_track()
            else:
                track_info = self.queue.pop_item()
                self.status.set_track(track_info)
                reversed_list = list(self.queue)
                reversed_list.reverse()
                self.status.update_queue(reversed_list)
        else:
            track_info = self.queue.pop_item()
            self.status.set_track(track_info)
            reversed_list = list(self.queue)
            reversed_list.reverse()
            self.status.update_queue(reversed_list)
        if not track_info:
            global_settings.gui_service.quick_gui(
                f"There is no track available to play",
                text_type='header',
                box_align='left')
            return
        self.callback_check('on_play')
        if global_settings.vlc_inst:
            audio_interface.stop_vlc_instance()
        audio_interface.create_vlc_instance(self.status.get_track().uri, skipto=self.status['progress_time'])
        self.status['start_time'] = int(time())
        self.status.set_status(TrackStatus.PLAYING)
        if not track_info.quiet:
            self.display_playing_gui()

    def calculate_progress(self):
        if self.status.is_playing():
            if self.status['progress_time'] == 0:
                if self.status['pause_time'] == 0:
                    self.status['progress_time'] = int(time()) - self.status['start_time']
                else:
                    self.status['progress_time'] = self.status['pause_time'] - self.status['start_time']
            else:
                if self.status['pause_time'] == 0:
                    self.status['progress_time'] = int(time()) - self.status['start_time']
                else:
                    if self.status['pause_time'] != self.status['start_time']:
                        self.status['progress_time'] = self.status['progress_time'] + (
                                self.status['pause_time'] - self.status['start_time'])
                    else:
                        self.status['progress_time'] = self.status['progress_time'] + (
                                int(time()) - self.status['start_time'])
                        self.status['start_time'] = int(time())
                        self.status['pause_time'] = int(time())

    def pause(self):
        if self.status.is_playing():
            if global_settings.vlc_inst:
                audio_interface.stop_vlc_instance()
            self.calculate_progress()
            self.status['pause_time'] = int(time())

            self.status.set_status(TrackStatus.PAUSED)
            global_settings.gui_service.quick_gui(
                f"Paused track at {self.audio_utilities.sec_formatted(self.status['progress_time'])}",
                text_type='header',
                box_align='left')

    def resume(self):
        if self.status.is_paused():
            self.status['start_time'] = int(time())
            self.status['pause_time'] = int(time())
            self.play()

    def skip(self, track_number):
        if self.queue.is_empty():
            return
        if track_number > self.queue.size() - 1:
            return

        for i in range(track_number):
            self.queue.pop_item()
        reversed_list = list(self.queue)
        reversed_list.reverse()
        self.status.update_queue(reversed_list)

        self.callback_check('on_skip')
        if global_settings.vlc_inst:
            audio_interface.stop_vlc_instance()

        if track_number == 0:
            global_settings.gui_service.quick_gui(
                f"Skipping to next track in the audio queue.",
                text_type='header',
                box_align='left')
        else:
            global_settings.gui_service.quick_gui(
                f"Skipping to track {track_number} in the audio queue.",
                text_type='header',
                box_align='left')

        self.status['start_time'] = int(time())
        self.status['pause_time'] = 0
        self.status['progress_time'] = 0

        self.play(override=True)

    def replay(self):
        self.seek(0)

    def shuffle(self):
        if self.queue.is_empty():
            return
        self.queue.shuffle()
        reversed_list = list(self.queue)
        reversed_list.reverse()
        self.status.update_queue(reversed_list)
        global_settings.gui_service.quick_gui(
            f"Shuffled the audio queue.",
            text_type='header',
            box_align='left')

    def seek(self, seconds: int):
        if self.status.is_playing():
            if global_settings.vlc_inst:
                audio_interface.stop_vlc_instance()
            audio_interface.create_vlc_instance(self.status.get_track().uri, skipto=seconds)

            self.status['start_time'] = int(time())
            self.status['pause_time'] = int(time())
            self.status['progress_time'] = int(seconds)

            global_settings.gui_service.quick_gui(
                f"Skipped to {str(timedelta(seconds=int(seconds)))} in the audio track.",
                text_type='header',
                box_align='left')

    def stop(self):
        if global_settings.vlc_inst:
            audio_interface.stop_vlc_instance()
        self.callback_check('on_stop')
        self.queue = queue_handler.QueueHandler([], maxlen=int(
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_QUEUE_LEN]))
        self.status.update({
            'plugin_owner': '',
            'plugin_name': '',
            'sender': '',
            'track': TrackInfo(uri='', name='', sender='', duration=-1, track_type=TrackType.FILE),
            'track_uri': '',
            'alt_uri': '',
            'image_uri': '',
            'track_id': '',
            'queue': [],
            'queue_length': 0,
            'status': TrackStatus.STOPPED,
            'pause_time': 0,
            'start_time': 0,
            'progress_time': 0,
            'volume': self.status['volume'],
            'loop': self.status['loop'],
            'duck_audio': self.status['duck_audio'],
            'ducking_volume': self.status['ducking_volume'],
            'ducking_threshold': self.status['ducking_threshold'],
            'ducking_delay': self.status['ducking_delay'],
            # Internal Audio Ducking Settings
            'is_ducking': False,
            'duck_start': 0.0,
            'duck_end': 0.0,
            'last_volume': self.status['last_volume']
        })
        self.clear_dni()

    def reset(self):
        self.callback_check('on_reset')
        self.queue = queue_handler.QueueHandler([], maxlen=int(
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_QUEUE_LEN]))
        self.status.update({
            'plugin_owner': '',
            'plugin_name': '',
            'sender': '',
            'track': TrackInfo(uri='', name='', sender='', duration=-1, track_type=TrackType.FILE),
            'track_uri': '',
            'alt_uri': '',
            'image_uri': '',
            'track_id': '',
            'queue': [],
            'queue_length': 0,
            'status': TrackStatus.STOPPED,
            'pause_time': 0,
            'start_time': 0,
            'progress_time': 0,
            'volume': self.status['volume'],
            'loop': self.status['loop'],
            'duck_audio': self.status['duck_audio'],
            'ducking_volume': self.status['ducking_volume'],
            'ducking_threshold': self.status['ducking_threshold'],
            'ducking_delay': self.status['ducking_delay'],
            # Internal Audio Ducking Settings
            'is_ducking': False,
            'duck_start': 0.0,
            'duck_end': 0.0,
            'last_volume': self.status['last_volume']
        })
        self.clear_dni()

    def clear_queue(self):
        self.queue = queue_handler.QueueHandler([], maxlen=int(
            global_settings.cfg[C_MEDIA_SETTINGS][P_MEDIA_VLC_QUEUE_LEN]))
        self.status.update_queue(list(self.queue))

    def enqueue_track(self, track_obj, to_front=False, quiet=False):
        if self.queue.is_full():
            if not quiet:
                global_settings.gui_service.quick_gui(
                    "Cannot add any more tracks because the audio queue is full!",
                    text_type='header',
                    box_align='left')
            return
        # Calculate track duration if a file is provided.
        if track_obj.track_type == TrackType.FILE and not track_obj.duration:
            try:
                with wave.open(track_obj.uri, 'r') as wfile:
                    frames = wfile.getnframes()
                    rate = wfile.getframerate()
                    raw_length = frames / float(rate)
                    track_length = str(timedelta(seconds=round(raw_length))) if raw_length > 0 else -1
            except wave.Error:
                track_length = -1
            except EOFError:
                track_length = -1
            track_obj.duration = track_length
        elif track_obj.track_type == TrackType.STREAM and not track_obj.duration:
            track_obj.duration = -1
        # New tracks must have a non-empty name.
        if track_obj.name == '':
            return
        # Enqueue the track based on priority.
        if to_front:
            self.queue.insert_priority_item(track_obj)
        else:
            self.queue.insert_item(track_obj)
        # Update interface status
        reversed_list = list(self.queue)
        reversed_list.reverse()
        self.status.update_queue(reversed_list)
        if not quiet:
            global_settings.gui_service.quick_gui(
                f"{track_obj.sender} added <font color={global_settings.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{track_obj.name}</font> to the audio queue.",
                text_type='header',
                box_align='left')

    def loop_track(self):
        if self.status.is_looping():
            self.status.disable_loop()
            return
        self.status.enable_loop()

    def remove_track(self, track_index=0, track_name=None):
        # Search and remove first occurrence of track by name.
        if track_name:
            track_index = None
            for i, track_info in enumerate(self.status['queue']):
                if track_info.name == track_name:
                    track_index = i
                    break
            if track_index:
                self.queue.remove_item(track_index)
        # Remove track at the given index.
        else:
            if track_index > self.queue.size() - 1:
                return
            self.queue.remove_item(track_index)
        reversed_list = list(self.queue)
        reversed_list.reverse()
        self.status.update_queue(reversed_list)

    def next_track(self):
        # Execute any callbacks subscribed to next_track
        self.callback_check('on_next_track')

        self.status['start_time'] = int(time())
        self.status['pause_time'] = 0
        self.status['progress_time'] = 0
        if self.status.is_looping() and self.status.get_track().alt_uri != '':
            self.status.set_status(TrackStatus.PLAYING)
            return True
        track_to_play = self.queue.pop_item()
        if track_to_play:
            self.status.set_track(track_obj=track_to_play)
            reversed_list = list(self.queue)
            reversed_list.reverse()
            self.status.update_queue(reversed_list)
            self.callback_check('song_integrity_check')
            if not track_to_play.quiet:
                self.display_playing_gui()
            self.status.set_status(TrackStatus.PLAYING)
            return True
        return False

    def get_track(self):
        return self.status.get_track()

    def display_playing_gui(self):
        cur_track_hashed_img_uri = hex(crc32(str.encode(self.get_track().track_id)) & 0xffffffff)
        if self.get_track().track_type == TrackType.FILE:
            cur_track = self.status.get_track()
            global_settings.gui_service.quick_gui(
                f"<font color={global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{'Now playing' if self.status.is_playing() else 'Paused'}</font>[{cur_track.track_type.value}"
                f"({self.audio_utilities.sec_formatted(self.status['progress_time']) + '-' if (self.status['progress_time']) > 0 else ''}{cur_track.duration})]: "
                f"{'<br>' if len(cur_track.name) > 40 else ''}<font color={global_settings.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{cur_track.name}</font> by {cur_track.sender}",
                text_type='header',
                box_align='left')
        elif self.get_track().track_type == TrackType.STREAM and self.get_track().image_uri and self.get_track().track_id:
            image_uri_split = self.get_track().image_uri.rsplit('/', 1)
            image_dir = image_uri_split[0]
            image_file = cur_track_hashed_img_uri
            cur_track = self.status.get_track()
            if os.path.exists(f"{image_dir}/{image_file}.jpg"):
                global_settings.gui_service.quick_gui_img(
                    image_dir,
                    image_file,
                    caption=f"<font color={global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{'Now playing' if self.status.is_playing() else 'Paused'}</font>[{cur_track.track_type.value}"
                            f"({self.audio_utilities.sec_formatted(self.status['progress_time']) + '-' if (self.status['progress_time']) > 0 else ''}{cur_track.duration})]: "
                            f"{'<br>' if len(cur_track.name) > 40 else ''}<font color={global_settings.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{cur_track.name}</font> by {cur_track.sender}",
                    caption_align='left',
                    format_img=True,
                    img_size=32768
                )
            else:
                from JJMumbleBot.lib.utils.dir_utils import get_main_dir
                global_settings.gui_service.quick_gui_img(
                    f'{get_main_dir()}/lib/images',
                    f'img_unavailable',
                    caption=f"<font color={global_settings.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>{'Now playing' if self.status.is_playing() else 'Paused'}</font>[{cur_track.track_type.value}"
                            f"({self.audio_utilities.sec_formatted(self.status['progress_time']) + '-' if (self.status['progress_time']) > 0 else ''}{cur_track.duration})]: "
                            f"{'<br>' if len(cur_track.name) > 40 else ''}<font color={global_settings.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{cur_track.name}</font> by {cur_track.sender}",
                    caption_align='left',
                    format_img=True,
                    img_size=32768
                )

    def check_dni(self, plugin_name, quiet=False):
        if global_settings.audio_dni == plugin_name or not global_settings.audio_dni:
            return True
        if not quiet:
            dprint(
                f'An audio plugin({global_settings.audio_dni}) is already using the audio interface.')
            global_settings.gui_service.quick_gui(
                f"An audio plugin({global_settings.audio_dni}) is already using the audio interface.",
                text_type='header',
                box_align='left')
        return False

    def check_dni_is_mine(self, plugin_name):
        if global_settings.audio_dni == plugin_name:
            return True
        return False

    def check_dni_active(self):
        if global_settings.audio_dni:
            return True
        return False

    def set_dni(self, plugin_name, plugin_title):
        global_settings.audio_dni = plugin_name
        self.status['plugin_name'] = plugin_name
        self.status.set_plugin_owner(plugin_title)

    def clear_dni(self):
        global_settings.audio_dni = None
        self.status['plugin_name'] = ''
        self.status.clear_plugin_owner()
