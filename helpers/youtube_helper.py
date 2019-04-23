import time
from helpers.global_access import GlobalMods as GM


def next_track(song_info):
    if song_info['main_dur'] is 0:
        return
    time.sleep(song_info['main_dur'])

    song_info['text_info'].message = '!snext'
    GM.jjmumblebot.process_remote_command(song_info['text_info'])
