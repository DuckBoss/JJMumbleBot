from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def cmd_audiostatus(self, data):
        gs.gui_service.quick_gui(
            str(gs.vlc_interface.status),
            text_type='header',
            box_align='left',
            text_align='left',
            ignore_whisper=True,
            user=gs.mumble_inst.users[data.actor]['name']
        )

    def cmd_stop(self, data):
        if gs.vlc_interface.check_dni_active():
            gs.vlc_interface.stop()
            gs.gui_service.quick_gui("Stopped bot audio.", text_type='header',
                                     box_align='left')

    def cmd_playing(self, data):
        if gs.vlc_interface.check_dni_active():
            track_info = gs.vlc_interface.status.get_track()
            rprint(
                f'{get_bot_name()}({gs.vlc_interface.status.get_plugin_owner()}) is playing: {track_info.name} (duration: {track_info.duration})',
                origin=L_COMMAND)
            gs.gui_service.quick_gui(
                f'{get_bot_name()}({gs.vlc_interface.status.get_plugin_owner()}) is playing: {track_info.name} (duration: {track_info.duration})',
                text_type='header',
                box_align='left')

    def cmd_skip(self, data):
        if gs.vlc_interface.check_dni_active():
            all_data = data.message.strip().split(' ', 1)
            try:
                skip_to = int(all_data[1])
            except ValueError:
                return
            except IndexError:
                skip_to = 0
            gs.vlc_interface.skip(skip_to)

    def cmd_shuffle(self, data):
        if gs.vlc_interface.check_dni_active():
            gs.vlc_interface.shuffle()

    def cmd_loop(self, data):
        gs.vlc_interface.loop_track()
        gs.gui_service.quick_gui(
            f"{'Enabled' if gs.vlc_interface.status.is_looping() else 'Disabled'} track looping.",
            text_type='header',
            box_align='left')

    def cmd_remove(self, data):
        if gs.vlc_interface.check_dni_active():
            all_data = data.message.strip().split(' ', 1)
            try:
                to_remove = int(all_data[1])
            except ValueError:
                return
            except IndexError:
                return
            gs.vlc_interface.remove_track(track_index=to_remove)

    def cmd_seek(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            return
        if gs.vlc_interface.check_dni_active():
            try:
                gs.vlc_interface.seek(int(all_data[1]))
            except ValueError:
                return

    def cmd_duckaudio(self, data):
        gs.vlc_interface.audio_utilities.toggle_ducking()
        gs.gui_service.quick_gui(
            f"{'Enabled' if gs.vlc_interface.audio_utilities.can_duck() else 'Disabled'} audio volume ducking.",
            text_type='header',
            box_align='left')
        log(INFO, f"Audio ducking was {'enabled' if gs.vlc_interface.audio_utilities.can_duck() else 'disabled'}.", origin=L_COMMAND)

    def cmd_duckvolume(self, data):
        try:
            vol = float(data.message.strip().split(' ', 1)[1])
        except IndexError:
            gs.gui_service.quick_gui(
                f"Current bot ducking volume: {gs.vlc_interface.audio_utilities.get_ducking_volume()}",
                text_type='header',
                box_align='left')
            return
        if vol > 1 or vol < 0:
            gs.gui_service.quick_gui(
                "Invalid Volume Input: [0-1]",
                text_type='header',
                box_align='left')
            return

        gs.vlc_interface.audio_utilities.set_duck_volume(vol)
        gs.gui_service.quick_gui(
            f"Set volume to {vol}",
            text_type='header',
            box_align='left')
        log(INFO, f"The bot audio ducking volume was changed to {vol}.", origin=L_COMMAND)

    def cmd_volume(self, data):
        try:
            vol = float(data.message.strip().split(' ', 1)[1])
        except IndexError:
            gs.gui_service.quick_gui(
                f"Current bot volume: {gs.vlc_interface.status.get_volume()}",
                text_type='header',
                box_align='left')
            return
        if vol > 1 or vol < 0:
            gs.gui_service.quick_gui(
                "Invalid Volume Input: [0-1]",
                text_type='header',
                box_align='left')
            return
        if gs.vlc_interface.audio_utilities.is_ducking():
            gs.vlc_interface.audio_utilities.set_last_volume(vol)
        else:
            gs.vlc_interface.audio_utilities.set_volume(vol, auto=False)
        gs.gui_service.quick_gui(
            f"Set volume to {vol}",
            text_type='header',
            box_align='left')
        log(INFO, f"The volume was changed to {vol}.", origin=L_COMMAND)

    def cmd_duckthreshold(self, data):
        try:
            threshold = float(data.message.strip().split(' ', 1)[1])
        except IndexError:
            gs.gui_service.quick_gui(
                f"Current bot ducking threshold: {gs.vlc_interface.audio_utilities.get_ducking_threshold()}",
                text_type='header',
                box_align='left')
            return
        if threshold < 0:
            gs.gui_service.quick_gui(
                "Invalid Ducking Threshold Input: [Recommended: 3000]",
                text_type='header',
                box_align='left')
            return

        gs.vlc_interface.audio_utilities.set_duck_threshold(threshold)
        gs.gui_service.quick_gui(
            f"Set ducking threshold to {threshold}",
            text_type='header',
            box_align='left')
        log(INFO, f"The bot audio ducking threshold was changed to {threshold}.", origin=L_COMMAND)

    def cmd_duckdelay(self, data):
        try:
            delay = float(data.message.strip().split(' ', 1)[1])
        except IndexError:
            gs.gui_service.quick_gui(
                f"Current bot ducking delay: {gs.vlc_interface.audio_utilities.get_ducking_delay()}",
                text_type='header',
                box_align='left')
            return
        if delay < 0 or delay > 5:
            gs.gui_service.quick_gui(
                "Invalid Ducking Delay Input: [0-5]",
                text_type='header',
                box_align='left')
            return

        gs.vlc_interface.audio_utilities.set_ducking_delay(delay)
        gs.gui_service.quick_gui(
            f"Set ducking delay to {delay}",
            text_type='header',
            box_align='left')
        log(INFO, f"The bot audio ducking delay was changed to {delay}.", origin=L_COMMAND)