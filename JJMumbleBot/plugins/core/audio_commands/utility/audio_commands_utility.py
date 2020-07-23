from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.vlc.vlc_api import TrackType


def get_queue_list():
    list_queue = []
    queue_list = list(gs.vlc_interface.status.get_queue())
    for i, track_info in enumerate(queue_list):
        if i == 0:
            list_queue.append(
                f"<br><font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[Up Next]</font> - "
                f"<a href='{track_info.uri if track_info.track_type == TrackType.FILE else track_info.alt_uri}'>{track_info.name}</a>")
        else:
            list_queue.append(
                f"<br><font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - "
                f"<a href='{track_info.uri if track_info.track_type == TrackType.FILE else track_info.alt_uri}'>{track_info.name}</a>")
    return list_queue
