from JJMumbleBot.lib.utils.print_utils import dprint
import requests


class VLCInterface:
    def __init__(self, web_host, web_port, web_user, web_pass):
        self.vlc_host = web_host
        self.vlc_port = web_port
        self.vlc_user = web_user
        self.vlc_pass = web_pass

    def get_status_json(self):
        try:
            web_resp = requests.get(f'http://{self.vlc_host}:{self.vlc_port}/requests/status.json',
                                    auth=(self.vlc_user, self.vlc_pass))
            if web_resp.ok:
                return web_resp.json()
            return None
        except requests.RequestException as e:
            dprint(e)
            return None

    def get_playlist_json(self):
        try:
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/playlist.json',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok:
                return web_resp.content
            return None
        except requests.RequestException as e:
            dprint(e)
            return None

    def toggle_pause(self, pause=True) -> bool:
        try:
            current_json = self.get_status_json()
            if current_json:
                if (current_json['state'] == 'playing' and pause is True) or (
                        current_json['state'] == 'paused' and pause is False):
                    web_resp = requests.post(
                        f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_pause',
                        auth=(self.vlc_user, self.vlc_pass)
                    )
                    if web_resp.ok:
                        return True
                    return False
                elif current_json['state'] == 'stopped':
                    self.play()
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def get_playlist(self):
        playlist_json = self.get_playlist_json()
        if playlist_json:
            current_playlist = []
            for track in playlist_json['children']['children']:
                current_track = playlist_json['children']['children'][track]
                current_track_dict = {
                    "name": current_track['name'],
                    "duration": current_track['duration'],
                    "track_id": current_track['id'],
                    "uri": current_track['uri'],
                    "current": current_track['current']
                }
                current_playlist.append(current_track_dict)
            return current_playlist
        return None

    def clear_playlist(self) -> bool:
        try:
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_empty',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok:
                return True
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def add_to_playlist(self, mrl=None) -> bool:
        try:
            if mrl is None:
                return False
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=in_enqueue&input={mrl}',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok:
                return True
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def add_and_play_to_playlist(self, mrl=None):
        try:
            if mrl is None:
                return False
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=in_play&input={mrl}',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok:
                return True
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def next_track(self) -> bool:
        try:
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_next',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok:
                return True
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def last_track(self) -> bool:
        try:
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_previous',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok:
                return True
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def play(self) -> bool:
        try:
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_play',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok:
                return True
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def play_specific(self, track_id: int):
        try:
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_play&id={int(track_id)}',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok:
                return True
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def stop(self) -> bool:
        try:
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_stop',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok and self.clear_playlist():
                return True
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def seek(self, seconds: int = 0) -> bool:
        try:
            current_json = self.get_status_json()
            if current_json:
                if seconds > int(current_json['length']):
                    self.stop()
                    return True
                web_resp = requests.post(
                    f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=seek&val={seconds}',
                    auth=(self.vlc_user, self.vlc_pass)
                )
                if web_resp.ok:
                    return True
                return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def sort(self, sort_mode: int = 0) -> bool:
        try:
            web_resp = requests.post(
                f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_sort&id=0&val={sort_mode}',
                auth=(self.vlc_user, self.vlc_pass)
            )
            if web_resp.ok:
                return True
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def toggle_loop(self, loop=True) -> bool:
        try:
            current_json = self.get_status_json()
            if current_json:
                if (current_json['loop'] is False and loop is True) or (
                        current_json['loop'] is True and loop is False):
                    web_resp = requests.post(
                        f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_loop',
                        auth=(self.vlc_user, self.vlc_pass)
                    )
                    if web_resp.ok:
                        return True
                    return False
            return False
        except requests.RequestException as e:
            dprint(e)
            return False

    def toggle_repeat(self, repeat=True) -> bool:
        try:
            current_json = self.get_status_json()
            if current_json:
                if (current_json['repeat'] is False and repeat is True) or (
                        current_json['repeat'] is True and repeat is False):
                    web_resp = requests.post(
                        f'http://{self.vlc_host}:{self.vlc_port}/requests/status.xml?command=pl_repeat',
                        auth=(self.vlc_user, self.vlc_pass)
                    )
                    if web_resp.ok:
                        return True
                    return False
            return False
        except requests.RequestException as e:
            dprint(e)
            return False


class VLCStatus(VLCInterface):
    def __init__(self, web_host, web_port, web_user, web_pass):
        super().__init__(web_host, web_port, web_user, web_pass)

    def get_current_time(self):
        vlc_json = self.get_status_json()
        if vlc_json:
            return vlc_json['time']
        return None

    def get_track_length(self):
        vlc_json = self.get_status_json()
        if vlc_json:
            return vlc_json['length']
        return None

    def is_looping(self) -> bool:
        vlc_json = self.get_status_json()
        if vlc_json:
            return vlc_json['loop']
        return False

    def is_repeating(self) -> bool:
        vlc_json = self.get_status_json()
        if vlc_json:
            return vlc_json['repeat']
        return False

    def is_playing(self) -> bool:
        vlc_json = self.get_status_json()
        if vlc_json:
            if vlc_json['state'] == 'playing':
                return True
        return False

    def is_paused(self) -> bool:
        vlc_json = self.get_status_json()
        if vlc_json:
            if vlc_json['state'] == 'paused':
                return True
        return False