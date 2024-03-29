from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.core.server_tools.resources.strings import *
from JJMumbleBot.plugins.core.server_tools.utility import settings as st_settings, server_tools_utility as st_utility
from JJMumbleBot.plugins.extensions.sound_board.utility.sound_board_utility import find_file
from JJMumbleBot.lib.utils.runtime_utils import get_command_token, get_users_in_my_channel
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.audio.audio_api import TrackType, TrackInfo, AudioLibrary
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name
from os import path


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/{self.plugin_name}/')
        self.is_running = True
        st_settings.server_tools_metadata = self.metadata
        st_settings.plugin_name = self.plugin_name
        if not st_utility.create_empty_user_connections():
            self.quit()
        self.register_callbacks()
        log(
            INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value
        )

    def quit(self):
        if gs.aud_interface.check_dni_is_mine(self.plugin_name):
            gs.aud_interface.stop()
            gs.audio_dni = None
        dir_utils.clear_directory(f'{dir_utils.get_temp_med_dir()}/{self.plugin_name}')
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

    def register_callbacks(self):
        from pymumble_py3.constants import PYMUMBLE_CLBK_USERCREATED
        st_utility.read_user_connections()
        if self.metadata.getboolean(C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False):
            gs.core_callbacks.append_to_callback(PYMUMBLE_CLBK_USERCREATED, self.clbk_user_connected)
            log(INFO, "Registered server_tools plugin callbacks", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def clbk_user_connected(self, user):
        # Display the welcome message to the user if any.
        if self.metadata.getboolean(C_PLUGIN_SET, P_USE_WELCOME_MSG, fallback=False):
            if len(self.metadata[C_PLUGIN_SET][P_WELCOME_MSG]) > 0:
                gs.gui_service.quick_gui(f"{self.metadata[C_PLUGIN_SET][P_WELCOME_MSG]}",
                                         text_type='header',
                                         box_align='left',
                                         user=user[0]['name'])

        # Return if the user that connected is the bot (self-detection).
        if len(get_users_in_my_channel()) == 1:
            return

        # Return if playing audio clips on user join is disabled.
        if not self.metadata.getboolean(C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False):
            return

        if gs.aud_interface.check_dni(self.plugin_name, quiet=True):
            gs.aud_interface.set_dni(self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME])
        else:
            return

        to_play = None
        # If playing the same clip on user join is enabled, load the generic clip name.
        # Otherwise, load the clip name set to the user.
        if self.metadata.getboolean(C_PLUGIN_SET, P_PLAY_SAME_CLIP_ON_USER_JOIN, fallback=True):
            to_play = self.metadata[C_PLUGIN_SET][P_GENERIC_CLIP_TO_PLAY_ON_USER_JOIN]
        else:
            to_play = st_settings.user_connections.get(user[0]['name'])

        # If to_play doesn't exist, that means the user is not on the user_connections.csv file.
        # use the built-in clip when the user isn't on the list.
        if not to_play:
            to_play = self.metadata[C_PLUGIN_SET][P_GENERIC_CLIP_TO_PLAY_ON_USER_JOIN]

        # If the clip is only allowed to play when other users are in the channel
        # and no users are present, clear DNI and return.
        if self.metadata.getboolean(C_PLUGIN_SET, P_PLAY_CLIP_ONLY_IF_USERS_IN_CHANNEL, fallback=True):
            if len(get_users_in_my_channel()) <= 1:
                gs.aud_interface.clear_dni()
                return

        # Find and load the clip, then play it.
        audio_clip = find_file(to_play)
        if not audio_clip:
            if not self.metadata.getboolean(C_PLUGIN_SET, P_USE_BUILT_IN_CLIP, fallback=True):
                gs.aud_interface.clear_dni()
                log(ERROR, f"The audio clip: {to_play} for the user connection sound could not be found.", origin=L_COMMAND,
                    error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
                gs.gui_service.quick_gui(f"The audio clip: {to_play} for the user connection sound could not be found.",
                                         text_type='header',
                                         box_align='left')
                return
            track_obj = TrackInfo(
                uri=f'{dir_utils.get_core_plugin_dir()}/server_tools/resources/default_user_sound.wav',
                alt_uri=f'{dir_utils.get_core_plugin_dir()}/server_tools/resources/default_user_sound.wav',
                name='default_user_sound.wav',
                sender=get_bot_name(),
                duration=None,
                track_type=TrackType.FILE,
                quiet=True
            )
        else:
            # If the plugin is set to use sound board clips, retrieve the clip from the sound board media directory.
            if self.metadata.getboolean(C_PLUGIN_SET, P_USE_SOUNDBOARD_CLIPS, fallback=True):
                track_obj = TrackInfo(
                    uri=f'{dir_utils.get_perm_med_dir()}/sound_board/{audio_clip}',
                    alt_uri=f'{dir_utils.get_perm_med_dir()}/sound_board/{audio_clip}',
                    name=to_play,
                    sender=get_bot_name(),
                    duration=None,
                    track_type=TrackType.FILE,
                    quiet=True
                )
            else:
                # Otherwise, retrieve the clip from the server tools plugin media directory.
                track_obj = TrackInfo(
                    uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
                    alt_uri=f'{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{audio_clip}',
                    name=to_play,
                    sender=get_bot_name(),
                    duration=None,
                    track_type=TrackType.FILE,
                    quiet=True
                )
        gs.aud_interface.enqueue_track(
            track_obj=track_obj,
            to_front=False,
            quiet=True
        )
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG, override=True)

    def cmd_wiki(self, data):
        gs.gui_service.quick_gui(f'<a href="{LINK_WIKI}">Visit the JJMumbleBot Wiki</a>', text_type='header', box_align='left',
                                 text_align='left', user=gs.mumble_inst.users[data.actor]['name'],
                                 ignore_whisper=True)
        log(INFO, f"Displayed wiki hyperlink to the user: {gs.mumble_inst.users[data.actor]['name']}",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_toggleloginsounds(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        current_status = not self.metadata.getboolean(C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False)
        self.metadata[C_PLUGIN_SET][P_PLAY_AUDIO_CLIP_ON_USER_JOIN] = f"{'True' if current_status else 'False'}"
        try:
            with open(f'{dir_utils.get_core_plugin_dir()}/{self.plugin_name}/metadata.ini', 'w') as metadata_file:
                self.metadata.write(metadata_file)
            self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
            log(INFO, f"{'Enabled' if current_status else 'Disabled'} user connection sounds in the server_tools metadata.ini file.",
                origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(f"{'Enabled' if current_status else 'Disabled'} user connection sounds in "
                                     f"the server_tools metadata.ini file.",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
        except IOError:
            log(ERROR, f"There was an error saving the {self.plugin_name} metadata to the metadata.ini file.", origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(f"There was an error saving the {self.plugin_name} metadata to the metadata.ini file.",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
            return

    def cmd_clearloginsound(self, data):
        all_data = data.message.strip().split(' ', 1)
        data_actor = gs.mumble_inst.users[data.actor]
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_CLEAR_USER_CONNECTION, origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(CMD_INVALID_CLEAR_USER_CONNECTION,
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
            return
        username = all_data[1]
        if st_settings.user_connections.get(username):
            del st_settings.user_connections[username]
            st_utility.save_user_connections()
            log(INFO, f"Removed {username} from the user_connections.csv file.",
                origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(f"Removed {username} from the user_connections.csv file.",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])

    def cmd_setdefaultloginsound(self, data):
        all_data = data.message.strip().split(' ', 1)
        data_actor = gs.mumble_inst.users[data.actor]
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_SET_USER_DEFAULT_CONNECTION, origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(CMD_INVALID_SET_USER_DEFAULT_CONNECTION,
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
            return
        audio_clip_name = all_data[1]
        if not find_file(audio_clip_name):
            log(ERROR, f"{audio_clip_name} is not one of the available files in the sound board permanent directory.",
                origin=L_COMMAND, error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                f"{audio_clip_name} is not one of the available files in the sound board permanent directory.",
                text_type='header',
                box_align='left',
                user=data_actor['name'])
            return
        self.metadata[C_PLUGIN_SET][P_GENERIC_CLIP_TO_PLAY_ON_USER_JOIN] = audio_clip_name
        try:
            with open(f'{dir_utils.get_core_plugin_dir()}/{self.plugin_name}/metadata.ini', 'w') as metadata_file:
                self.metadata.write(metadata_file)
            self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{self.plugin_name}')
            log(INFO, f"Updated the default user connection sound and saved the {self.plugin_name} metadata to the metadata.ini file.",
                origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(
                f"Updated the default user connection sound and saved the {self.plugin_name} metadata to the metadata.ini file.",
                text_type='header',
                box_align='left',
                user=data_actor['name'])
        except IOError:
            log(ERROR, f"There was an error saving the {self.plugin_name} metadata to the metadata.ini file.",
                origin=L_COMMAND, error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(f"There was an error saving the {self.plugin_name} metadata to the metadata.ini file.",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
            return

    def cmd_setloginsound(self, data):
        all_data = data.message.strip().split(' ', 2)
        data_actor = gs.mumble_inst.users[data.actor]
        if len(all_data) != 3:
            log(ERROR, CMD_INVALID_SET_USER_CONNECTION,
                origin=L_COMMAND, error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(CMD_INVALID_SET_USER_CONNECTION,
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
            return
        username = all_data[1]
        track = all_data[2]
        st_settings.user_connections[username] = track
        st_utility.save_user_connections()
        if self.metadata.getboolean(C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False):
            gs.gui_service.quick_gui(f"Set {track} to play whenever {username} connects to the server.",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
        else:
            gs.gui_service.quick_gui(f"Set {track} to play whenever {username} connects to the server,"
                                     f"<br>however the bot isn't configured to play audio clips when a user joins."
                                     f"<br>This feature can be enabled in the {self.plugin_name} metadata.ini file."
                                     f"<br>For a list of available sound clips, use '{get_command_token()}sblist'",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
        log(INFO, f"Set user connection sound: {track} to play whenever {username} connects to the server.",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_getloginsound(self, data):
        all_data = data.message.strip().split(' ', 1)
        data_actor = gs.mumble_inst.users[data.actor]
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_GET_USER_CONNECTION,
                origin=L_COMMAND, error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(CMD_INVALID_GET_USER_CONNECTION,
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
            return

        username = all_data[1]
        st_utility.read_user_connections()
        if username not in st_settings.user_connections:
            log(ERROR, f"The provided username: {username} was not found in the user connections dictionary.",
                origin=L_COMMAND, error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(f"The provided username was not found in the user connections dictionary."
                                     f"<br>You can add a new username to the dictionary with '{get_command_token()}setuserconnectionsound'",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
            return
        if not st_settings.user_connections[username]:
            log(ERROR, f"The provided username: {username} was found but an audio track was not assigned to the user connection.",
                origin=L_COMMAND, error_type=CMD_PROCESS_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            gs.gui_service.quick_gui(f"The username was found but a sound clip was not assigned."
                                     f"<br>You can set a sound clip to the username with '{get_command_token()}setuserconnectionsound'"
                                     f"<br>For a list of available sound clips, use '{get_command_token()}sblist'",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
            return
        if self.metadata.getboolean(C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False):
            gs.gui_service.quick_gui(f"{st_settings.user_connections[username]} is set to play whenever {username} connects to the server.",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
        else:
            gs.gui_service.quick_gui(f"{st_settings.user_connections[username]} is set to play whenever {username} connects to the server,"
                                     f"<br>however the bot isn't configured to play audio clips when a user joins."
                                     f"<br>This feature can be enabled in the {self.plugin_name} metadata.ini file.",
                                     text_type='header',
                                     box_align='left',
                                     user=data_actor['name'])
