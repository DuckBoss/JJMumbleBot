from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.plugins.core.audio_commands.resources.strings import *
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.plugins.core.audio_commands.utility import audio_commands_utility as ac_utility
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.resources.log_strings import *


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from os import path
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.is_running = True
        log(
            INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value
        )

    def quit(self):
        self.is_running = False
        log(
            INFO,
            f"Exiting {self.plugin_name} plugin...",
            origin=L_SHUTDOWN,
            print_mode=PrintMode.REG_PRINT.value
        )

    def stop(self):
        if self.is_running:
            self.quit()

    def start(self):
        if not self.is_running:
            self.__init__()

    def cmd_audiostatus(self, data):
        gs.aud_interface.calculate_progress()
        gs.gui_service.quick_gui(
            str(gs.aud_interface.status),
            text_type='header',
            box_align='left',
            text_align='left',
            ignore_whisper=True,
            user=gs.mumble_inst.users[data.actor]['name']
        )
        log(INFO, INFO_DISPLAYED_STATUS, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_stop(self, data):
        if gs.aud_interface.check_dni_active():
            gs.aud_interface.stop()
            log(INFO, INFO_AUDIO_STOPPED, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(INFO_AUDIO_STOPPED,
                                     text_type='header',
                                     box_align='left',
                                     text_align='left')

    def cmd_clear(self, data):
        if gs.aud_interface.check_dni_active():
            gs.aud_interface.clear_queue()
            log(INFO, INFO_AUDIO_CLEARED_QUEUE, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(INFO_AUDIO_CLEARED_QUEUE,
                                     text_type='header',
                                     box_align='left',
                                     text_align='left')

    def cmd_playing(self, data):
        if gs.aud_interface.check_dni_active():
            gs.aud_interface.calculate_progress()
            gs.aud_interface.display_playing_gui()
            log(INFO, INFO_DISPLAYED_PLAYING, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_queue(self, data):
        if gs.aud_interface.check_dni_active():
            queue_list = ac_utility.get_queue_list()
            if len(queue_list) == 0:
                gs.gui_service.quick_gui(
                    f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>The audio queue is empty.</font>",
                    text_type='header',
                    box_align='left')
                return
            out_str = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Audio Queue:</font>"
            for i, item in enumerate(queue_list):
                out_str += item
            gs.gui_service.quick_gui(
                out_str,
                text_type='header',
                text_align='left',
                box_align='left')
            log(INFO, INFO_DISPLAYED_QUEUE, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_skip(self, data):
        if gs.aud_interface.check_dni_active():
            all_data = data.message.strip().split(' ', 1)
            try:
                skip_to = int(all_data[1])
            except ValueError:
                log(ERROR, CMD_INVALID_TRACK_NUMBER, origin=L_COMMAND,
                    error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
                gs.gui_service.quick_gui(CMD_INVALID_TRACK_NUMBER,
                                         text_type='header',
                                         box_align='left',
                                         text_align='left')
                return
            except IndexError:
                log(WARNING, WARN_INVALID_TRACK_INDEX, origin=L_COMMAND,
                    error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
                skip_to = 0
            gs.aud_interface.skip(skip_to)
            log(INFO, INFO_AUDIO_SKIPPED, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_pause(self, data):
        if gs.aud_interface.check_dni_active():
            gs.aud_interface.pause()
            log(INFO, INFO_AUDIO_PAUSED, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_resume(self, data):
        if gs.aud_interface.check_dni_active():
            if gs.aud_interface.status.is_paused():
                gs.aud_interface.resume()
                log(INFO, INFO_AUDIO_RESUMED, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_shuffle(self, data):
        if gs.aud_interface.check_dni_active():
            gs.aud_interface.shuffle()
            log(INFO, INFO_AUDIO_SHUFFLED, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_replay(self, data):
        if gs.aud_interface.check_dni_active():
            gs.aud_interface.replay()
            log(INFO, INFO_AUDIO_REPLAYED, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_loop(self, data):
        gs.aud_interface.loop_track()
        log(
            INFO,
            f"{'Enabled' if gs.aud_interface.status.is_looping() else 'Disabled'} track looping.",
            origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        gs.gui_service.quick_gui(f"{'Enabled' if gs.aud_interface.status.is_looping() else 'Disabled'} track looping.",
                                 text_type='header',
                                 box_align='left',
                                 text_align='left')

    def cmd_remove(self, data):
        if gs.aud_interface.check_dni_active():
            all_data = data.message.strip().split(' ', 1)
            try:
                to_remove = int(all_data[1])
            except ValueError:
                log(ERROR, CMD_INVALID_TRACK_NUMBER, origin=L_COMMAND,
                    error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
                gs.gui_service.quick_gui(CMD_INVALID_TRACK_NUMBER,
                                         text_type='header',
                                         box_align='left',
                                         text_align='left')
                return
            except IndexError:
                log(ERROR, CMD_INVALID_REMOVE, origin=L_COMMAND,
                    error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
                return
            gs.aud_interface.remove_track(track_index=to_remove)
            log(INFO, INFO_AUDIO_REMOVED, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_seek(self, data):
        all_data = data.message.strip().split()
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_SEEK_VALUE, origin=L_COMMAND,
                error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                CMD_INVALID_SEEK,
                text_type='header',
                box_align='left',
                text_align='left'
            )
            return
        if gs.aud_interface.check_dni_active():
            given_time = all_data[1]
            if ":" in given_time:
                time_split = given_time.split(':')
                try:
                    if len(time_split) == 1:
                        # No ':' separator means that it is in seconds, no minutes/hours
                        given_time = int(all_data[1])
                        gs.aud_interface.seek(given_time)
                    elif len(time_split) == 2:
                        # One ':' separators means that is in mins:secs, no hours
                        mins = int(time_split[0])
                        secs = int(time_split[1])
                        given_time = (mins * 60) + secs
                        gs.aud_interface.seek(given_time)
                    elif len(time_split) == 3:
                        # Two ':' separators means that it is in hrs:mins:secs
                        hours = int(time_split[0])
                        mins = int(time_split[1])
                        secs = int(time_split[2])
                        given_time = (hours * 3600) + (mins * 60) + secs
                        gs.aud_interface.seek(given_time)
                    log(INFO, INFO_AUDIO_SEEKED, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
                except ValueError:
                    log(ERROR, CMD_INVALID_SEEK_VALUE, origin=L_COMMAND,
                        error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
                    gs.gui_service.quick_gui(
                        CMD_INVALID_SEEK,
                        text_type='header',
                        box_align='left',
                        text_align='left'
                    )
                    return
            else:
                try:
                    gs.aud_interface.seek(int(all_data[1]))
                    log(INFO, INFO_AUDIO_SEEKED, origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
                except ValueError:
                    log(ERROR, CMD_INVALID_SEEK_VALUE, origin=L_COMMAND,
                        error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
                    gs.gui_service.quick_gui(
                        CMD_INVALID_SEEK,
                        text_type='header',
                        box_align='left',
                        text_align='left'
                    )

    def cmd_volume(self, data):
        try:
            vol = float(data.message.strip().split(' ', 1)[1])
        except IndexError:
            log(
                INFO,
                f"Displayed current audio volume: {gs.aud_interface.status.get_volume()}",
                origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value
                )
            gs.gui_service.quick_gui(
                f"Current audio volume: {gs.aud_interface.status.get_volume()}",
                text_type='header',
                box_align='left')
            return
        if vol > 1 or vol < 0:
            log(
                ERROR,
                CMD_INVALID_VOLUME,
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            gs.gui_service.quick_gui(CMD_INVALID_VOLUME,
                                     text_type='header',
                                     box_align='left',
                                     text_align='left')
            return
        if gs.aud_interface.audio_utilities.is_ducking():
            gs.aud_interface.audio_utilities.set_last_volume(vol)
        else:
            gs.aud_interface.audio_utilities.set_volume(vol, auto=False)
        log(
            INFO,
            f"Set volume to {vol}",
            origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        gs.gui_service.quick_gui(f"Set volume to {vol}",
                                 text_type='header',
                                 box_align='left',
                                 text_align='left')

    def cmd_duckaudio(self, data):
        gs.aud_interface.audio_utilities.toggle_ducking()
        log(
            INFO,
            f"{'Enabled' if gs.aud_interface.audio_utilities.can_duck() else 'Disabled'} audio volume ducking.",
            origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        gs.gui_service.quick_gui(f"{'Enabled' if gs.aud_interface.audio_utilities.can_duck() else 'Disabled'} audio volume ducking.",
                                 text_type='header',
                                 box_align='left',
                                 text_align='left')

    def cmd_duckvolume(self, data):
        try:
            vol = float(data.message.strip().split(' ', 1)[1])
        except IndexError:
            log(
                INFO,
                f"Displayed current bot ducking volume: {gs.aud_interface.audio_utilities.get_ducking_volume()}",
                origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            gs.gui_service.quick_gui(
                f"Current bot ducking volume: {gs.aud_interface.audio_utilities.get_ducking_volume()}",
                text_type='header',
                box_align='left',
                text_align='left'
            )
            return
        if vol > 1 or vol < 0:
            log(
                ERROR,
                CMD_INVALID_VOLUME,
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            gs.gui_service.quick_gui(CMD_INVALID_VOLUME,
                                     text_type='header',
                                     box_align='left',
                                     text_align='left')
            return

        gs.aud_interface.audio_utilities.set_duck_volume(vol)
        log(
            INFO,
            f"Set audio ducking volume to {vol}",
            origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        gs.gui_service.quick_gui(f"Set audio ducking volume to {vol}",
                                 text_type='header',
                                 box_align='left',
                                 text_align='left')

    def cmd_duckthreshold(self, data):
        try:
            threshold = float(data.message.strip().split(' ', 1)[1])
        except ValueError:
            log(
                ERROR,
                CMD_INVALID_DUCKING_THRESHOLD,
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            gs.gui_service.quick_gui(CMD_INVALID_DUCKING_THRESHOLD,
                                     text_type='header',
                                     box_align='left',
                                     text_align='left')
            return
        except IndexError:
            log(
                INFO,
                f"Displayed current bot ducking threshold: {gs.aud_interface.audio_utilities.get_ducking_threshold()}",
                origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            gs.gui_service.quick_gui(
                f"Current bot ducking threshold: {gs.aud_interface.audio_utilities.get_ducking_threshold()}",
                text_type='header',
                box_align='left',
                text_align='left'
            )
            return
        if threshold < 0:
            log(
                ERROR,
                CMD_INVALID_DUCKING_THRESHOLD,
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            gs.gui_service.quick_gui(CMD_INVALID_DUCKING_THRESHOLD,
                                     text_type='header',
                                     box_align='left',
                                     text_align='left')
            return

        gs.aud_interface.audio_utilities.set_duck_threshold(threshold)
        log(
            INFO,
            f"Set audio ducking threshold to {threshold}",
            origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        gs.gui_service.quick_gui(f"Set audio ducking threshold to {threshold}",
                                 text_type='header',
                                 box_align='left',
                                 text_align='left')

    def cmd_duckdelay(self, data):
        try:
            delay = float(data.message.strip().split(' ', 1)[1])
        except IndexError:
            log(
                INFO,
                f"Displayed current bot audio ducking delay: {gs.aud_interface.audio_utilities.get_ducking_delay()}",
                origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            gs.gui_service.quick_gui(
                f"Current bot audio ducking delay: {gs.aud_interface.audio_utilities.get_ducking_delay()}",
                text_type='header',
                box_align='left',
                text_align='left'
            )
            return
        if delay < 0 or delay > 5:
            log(
                ERROR,
                CMD_INVALID_DUCKING_DELAY,
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value
            )
            gs.gui_service.quick_gui(CMD_INVALID_DUCKING_DELAY,
                                     text_type='header',
                                     box_align='left',
                                     text_align='left')
            return

        gs.aud_interface.audio_utilities.set_ducking_delay(delay)
        log(
            INFO,
            f"Set audio ducking delay to {delay}",
            origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value
        )
        gs.gui_service.quick_gui(f"Set audio ducking delay to {delay}",
                                 text_type='header',
                                 box_align='left',
                                 text_align='left')
