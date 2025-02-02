from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.settings import global_settings as gs
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.core.server_tools.resources.strings import *
from JJMumbleBot.plugins.core.server_tools.utility import (
    settings as st_settings,
    server_tools_utility as st_utility,
)
from JJMumbleBot.lib.utils.runtime_utils import (
    get_command_token,
    get_users_in_my_channel,
)
from JJMumbleBot.lib.utils.dir_utils import (
    make_directory,
    clear_directory,
    get_temp_med_dir,
    get_core_plugin_dir,
    get_perm_med_dir,
)
from JJMumbleBot.lib.utils.dir_utils import find_file as du_find_file
from JJMumbleBot.lib.audio.audio_api import TrackType, TrackInfo, AudioLibrary
from JJMumbleBot.lib.utils.runtime_utils import get_bot_name
from os import path, listdir
from typing import Union


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads

        self.plugin_name = path.basename(__file__).rsplit(".")[0]
        self.metadata = PluginUtilityService.process_metadata(
            f"plugins/core/{self.plugin_name}"
        )
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        make_directory(
            f"{gs.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/"
        )
        make_directory(
            f"{gs.cfg[C_MEDIA_SETTINGS][P_TEMP_MED_DIR]}/{self.plugin_name}/"
        )
        self.default_audio_clip = "default_user_sound.wav"
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
            print_mode=PrintMode.REG_PRINT.value,
        )

    def quit(self):
        if gs.aud_interface.check_dni_is_mine(self.plugin_name):
            gs.aud_interface.stop()
            gs.audio_dni = None
        clear_directory(f"{get_temp_med_dir()}/{self.plugin_name}")
        self.is_running = False
        log(
            INFO,
            f"Exiting {self.plugin_name} plugin...",
            origin=L_SHUTDOWN,
            print_mode=PrintMode.REG_PRINT.value,
        )

    def stop(self):
        if self.is_running:
            self.quit()

    def start(self):
        if not self.is_running:
            self.__init__()

    def register_callbacks(self):
        from mumble.callbacks import CALLBACK

        st_utility.read_user_connections()
        if self.metadata.getboolean(
            C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False
        ):
            gs.core_callbacks.append_to_callback(
                CALLBACK.USER_CREATED, self.clbk_user_connected
            )
            log(
                INFO,
                "Registered server_tools plugin callbacks",
                origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )

    def util_find_file(self, file_name):
        if not path.exists(f"{get_perm_med_dir()}/sound_board/"):
            log(
                ERROR,
                f"The media directory for the 'server_tools' plugin is missing! "
                f"Please make sure that a permanent media directory is set in the bot config.ini file in order "
                f"for the 'server_tools' plugin to generate a media directory!",
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            return None
        for file_item in listdir(f"{get_perm_med_dir()}/{self.plugin_name}/"):
            if file_item.rsplit(".", 1)[0] == file_name:
                return file_item
        return None

    def util_find_sb_file(self, file_name):
        if not path.exists(f"{get_perm_med_dir()}/sound_board/"):
            log(
                ERROR,
                f"The media directory for the 'sound_board' plugin is missing! "
                f"If the 'sound_board' plugin is missing or removed, this path will not exist. "
                f"The 'metadata.ini' file of the 'server_tools' plugin needs to be modified to disable using "
                f"files from the sound board!",
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            return None
        for file_item in listdir(f"{get_perm_med_dir()}/sound_board/"):
            if file_item.rsplit(".", 1)[0] == file_name:
                return file_item
        return None

    def util_find_and_create_track(self, file_name) -> Union[TrackInfo, None]:
        if self.metadata.getboolean(
            C_PLUGIN_SET, P_USE_SOUNDBOARD_CLIPS, fallback=True
        ):
            if self.util_find_sb_file(file_name):
                return TrackInfo(
                    uri=f"{get_perm_med_dir()}/sound_board/{file_name}",
                    alt_uri=f"{get_perm_med_dir()}/sound_board/{file_name}",
                    name=file_name,
                    sender=get_bot_name(),
                    duration=None,
                    track_type=TrackType.FILE,
                    quiet=True,
                )
            return None
        else:
            if self.util_find_file(file_name):
                return TrackInfo(
                    uri=f"{get_perm_med_dir()}/{self.plugin_name}/{file_name}",
                    alt_uri=f"{get_perm_med_dir()}/{self.plugin_name}/{file_name}",
                    name=file_name,
                    sender=get_bot_name(),
                    duration=None,
                    track_type=TrackType.FILE,
                    quiet=True,
                )
            return None

    def clbk_user_connected(self, user):
        # Display the welcome message to the user if any.
        if self.metadata.getboolean(C_PLUGIN_SET, P_USE_WELCOME_MSG, fallback=False):
            if len(self.metadata[C_PLUGIN_SET][P_WELCOME_MSG]) > 0:
                gs.gui_service.quick_gui(
                    f"{self.metadata[C_PLUGIN_SET][P_WELCOME_MSG]}",
                    text_type="header",
                    box_align="left",
                    user=user[0]["name"],
                )

        # Return if the user that connected is the bot (self-detection).
        if len(get_users_in_my_channel()) == 1:
            return

        # Return if playing audio clips on user join is disabled.
        if not self.metadata.getboolean(
            C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False
        ):
            return

        # If the clip is only allowed to play when other users are in the channel
        # and no users are present, return immediately.
        if self.metadata.getboolean(
            C_PLUGIN_SET, P_PLAY_CLIP_ONLY_IF_USERS_IN_CHANNEL, fallback=True
        ):
            if len(get_users_in_my_channel()) <= 1:
                return

        # Set the audio interface ownership to the server_tools plugin.
        if gs.aud_interface.check_dni(self.plugin_name, quiet=True):
            gs.aud_interface.set_dni(
                self.plugin_name, self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]
            )
        else:
            return

        # If playing the same clip on user join is enabled, load the generic clip name.
        # Otherwise, load the clip name set to the user.
        if self.metadata.getboolean(
            C_PLUGIN_SET, P_PLAY_SAME_CLIP_ON_USER_JOIN, fallback=False
        ):
            to_play: str = self.metadata[C_PLUGIN_SET][
                P_GENERIC_CLIP_TO_PLAY_ON_USER_JOIN
            ]
            # Attempt to find the clip in the server_tools and sound_board media directories
            track_search = self.util_find_and_create_track(to_play)
            if track_search is not None:
                track_obj = track_search
            # If the clip is missing, attempt to find the default clip instead.
            else:
                # If the default clip is also missing, end the command and log the error
                if not du_find_file(
                    self.default_audio_clip,
                    f"{get_core_plugin_dir()}/{self.plugin_name}/resources/",
                ):
                    gs.aud_interface.clear_dni()
                    log(
                        ERROR,
                        f"The audio clip: {self.default_audio_clip} for the user connection sound could not be found! "
                        f"If the generic clip has not been customized, the default 'default_user_sound.wav' should "
                        f"be included in the plugin's resource folder by default, "
                        f"please notify the developer if it's missing!",
                        origin=L_COMMAND,
                        error_type=CMD_PROCESS_ERR,
                        print_mode=PrintMode.VERBOSE_PRINT.value,
                    )
                    return
                track_obj = TrackInfo(
                    uri=f"{get_core_plugin_dir()}/{self.plugin_name}/resources/{self.default_audio_clip}",
                    alt_uri=f"{get_core_plugin_dir()}/{self.plugin_name}/resources/{self.default_audio_clip}",
                    name=self.default_audio_clip,
                    sender=get_bot_name(),
                    duration=None,
                    track_type=TrackType.FILE,
                    quiet=True,
                )
        else:
            to_play = st_settings.user_connections.get(user[0]["name"])
            # If to_play doesn't exist, that means the user is not on the user_connections.csv file.
            # use the generic audio clip when the user isn't on the list.
            if not to_play:
                to_play = self.metadata[C_PLUGIN_SET][
                    P_GENERIC_CLIP_TO_PLAY_ON_USER_JOIN
                ]
                # If the clip is missing, end the command and log the error
                if not du_find_file(
                    to_play,
                    f"{get_core_plugin_dir()}/{self.plugin_name}/resources/",
                ):
                    gs.aud_interface.clear_dni()
                    log(
                        ERROR,
                        f"The audio clip: {to_play} user connection sound for {user[0]['name']} could not be found! "
                        f"If the generic clip has not been customized, the default 'default_user_sound.wav' should "
                        f"be included in the plugin's resource folder by default, "
                        f"please notify the developer if it's missing!",
                        origin=L_COMMAND,
                        error_type=CMD_PROCESS_ERR,
                        print_mode=PrintMode.VERBOSE_PRINT.value,
                    )
                    return
                track_obj = TrackInfo(
                    uri=f"{get_core_plugin_dir()}/{self.plugin_name}/resources/{self.default_audio_clip}",
                    alt_uri=f"{get_core_plugin_dir()}/{self.plugin_name}/resources/{self.default_audio_clip}",
                    name=self.default_audio_clip,
                    sender=get_bot_name(),
                    duration=None,
                    track_type=TrackType.FILE,
                    quiet=True,
                )
            else:
                # If the plugin is set to use sound board clips, retrieve the path from the sound board media directory.
                # Otherwise, retrieve the clip from the server tools plugin media directory.
                track_obj = self.util_find_and_create_track(to_play)
                if track_obj is None:
                    gs.aud_interface.clear_dni()
                    log(
                        ERROR,
                        f"The audio clip: {to_play} connection sound for the user {user[0]['name']} could not be found.",
                        origin=L_COMMAND,
                        error_type=CMD_PROCESS_ERR,
                        print_mode=PrintMode.VERBOSE_PRINT.value,
                    )
                    gs.gui_service.quick_gui(
                        f"The audio clip: {to_play} connection sound for the user {user[0]['name']} could not be found.",
                        text_type="header",
                        box_align="left",
                    )
                    return

        # Play the audio clip
        gs.aud_interface.enqueue_track(track_obj=track_obj, to_front=False, quiet=True)
        gs.aud_interface.play(audio_lib=AudioLibrary.FFMPEG, override=True)

    def cmd_wiki(self, data):
        gs.gui_service.quick_gui(
            f'<a href="{LINK_WIKI}">Visit the JJMumbleBot Wiki</a>',
            text_type="header",
            box_align="left",
            text_align="left",
            user=gs.mumble_inst.users[data.actor]["name"],
            ignore_whisper=True,
        )
        log(
            INFO,
            f"Displayed wiki hyperlink to the user: {gs.mumble_inst.users[data.actor]['name']}",
            origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value,
        )

    def cmd_toggleloginsounds(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        current_status = not self.metadata.getboolean(
            C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False
        )
        self.metadata[C_PLUGIN_SET][P_PLAY_AUDIO_CLIP_ON_USER_JOIN] = (
            f"{'True' if current_status else 'False'}"
        )
        try:
            with open(
                f"{get_core_plugin_dir()}/{self.plugin_name}/metadata.ini", "w"
            ) as metadata_file:
                self.metadata.write(metadata_file)
            self.metadata = PluginUtilityService.process_metadata(
                f"plugins/core/{self.plugin_name}"
            )
            log(
                INFO,
                f"{'Enabled' if current_status else 'Disabled'} user connection sounds in the server_tools metadata.ini file.",
                origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                f"{'Enabled' if current_status else 'Disabled'} user connection sounds in "
                f"the server_tools metadata.ini file.",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
        except IOError:
            log(
                ERROR,
                f"There was an error saving the {self.plugin_name} metadata to the metadata.ini file.",
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                f"There was an error saving the {self.plugin_name} metadata to the metadata.ini file.",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
            return

    def cmd_clearloginsound(self, data):
        all_data = data.message.strip().split(" ", 1)
        data_actor = gs.mumble_inst.users[data.actor]
        if len(all_data) != 2:
            log(
                ERROR,
                CMD_INVALID_CLEAR_USER_CONNECTION,
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                CMD_INVALID_CLEAR_USER_CONNECTION,
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
            return
        username = all_data[1]
        if st_settings.user_connections.get(username):
            del st_settings.user_connections[username]
            st_utility.save_user_connections()
            log(
                INFO,
                f"Removed {username} from the user_connections.csv file.",
                origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                f"Removed {username} from the user_connections.csv file.",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )

    def cmd_setdefaultloginsound(self, data):
        all_data = data.message.strip().split(" ", 1)
        data_actor = gs.mumble_inst.users[data.actor]
        if len(all_data) != 2:
            log(
                ERROR,
                CMD_INVALID_SET_USER_DEFAULT_CONNECTION,
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                CMD_INVALID_SET_USER_DEFAULT_CONNECTION,
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
            return
        audio_clip_name = all_data[1]

        # If the plugin is set to use sound board clips, check if the file exists in the sound board media directory.
        # Otherwise, check if the file exists in the server tools media directory.
        if self.metadata.getboolean(
            C_PLUGIN_SET, P_USE_SOUNDBOARD_CLIPS, fallback=True
        ):
            if self.util_find_sb_file(audio_clip_name) is None:
                log(
                    ERROR,
                    f"{audio_clip_name} is not one of the available files in the sound board media directory.",
                    origin=L_COMMAND,
                    error_type=CMD_PROCESS_ERR,
                    print_mode=PrintMode.VERBOSE_PRINT.value,
                )
                gs.gui_service.quick_gui(
                    f"{audio_clip_name} is not one of the available files in the sound board media directory.",
                    text_type="header",
                    box_align="left",
                    user=data_actor["name"],
                )
                return
        else:
            if self.util_find_file(audio_clip_name) is None:
                log(
                    ERROR,
                    f"{audio_clip_name} is not one of the available files in the server tools media directory.",
                    origin=L_COMMAND,
                    error_type=CMD_PROCESS_ERR,
                    print_mode=PrintMode.VERBOSE_PRINT.value,
                )
                gs.gui_service.quick_gui(
                    f"{audio_clip_name} is not one of the available files in the server tools media directory.",
                    text_type="header",
                    box_align="left",
                    user=data_actor["name"],
                )
                return

        self.metadata[C_PLUGIN_SET][P_GENERIC_CLIP_TO_PLAY_ON_USER_JOIN] = (
            audio_clip_name
        )
        try:
            with open(
                f"{get_core_plugin_dir()}/{self.plugin_name}/metadata.ini", "w"
            ) as metadata_file:
                self.metadata.write(metadata_file)
            self.metadata = PluginUtilityService.process_metadata(
                f"plugins/core/{self.plugin_name}"
            )
            log(
                INFO,
                f"Updated the default user connection sound and saved the {self.plugin_name} metadata to the metadata.ini file.",
                origin=L_COMMAND,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                f"Updated the default user connection sound and saved the {self.plugin_name} metadata to the metadata.ini file.",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
        except IOError:
            log(
                ERROR,
                f"There was an error saving the {self.plugin_name} metadata to the metadata.ini file.",
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                f"There was an error saving the {self.plugin_name} metadata to the metadata.ini file.",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
            return

    def cmd_setloginsound(self, data):
        all_data = data.message.strip().split(" ", 2)
        data_actor = gs.mumble_inst.users[data.actor]
        if len(all_data) != 3:
            log(
                ERROR,
                CMD_INVALID_SET_USER_CONNECTION,
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                CMD_INVALID_SET_USER_CONNECTION,
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
            return
        username = all_data[1]
        track = all_data[2]

        # If the plugin is set to use sound board clips, check if the file exists in the sound board media directory.
        # Otherwise, check if the file exists in the server tools media directory.
        if self.metadata.getboolean(
            C_PLUGIN_SET, P_USE_SOUNDBOARD_CLIPS, fallback=True
        ):
            if self.util_find_sb_file(track) is None:
                log(
                    ERROR,
                    f"{track} is not one of the available files in the sound board media directory.",
                    origin=L_COMMAND,
                    error_type=CMD_PROCESS_ERR,
                    print_mode=PrintMode.VERBOSE_PRINT.value,
                )
                gs.gui_service.quick_gui(
                    f"{track} is not one of the available files in the sound board media directory.",
                    text_type="header",
                    box_align="left",
                    user=data_actor["name"],
                )
                return
        else:
            if self.util_find_file(track) is None:
                log(
                    ERROR,
                    f"{track} is not one of the available files in the server tools media directory.",
                    origin=L_COMMAND,
                    error_type=CMD_PROCESS_ERR,
                    print_mode=PrintMode.VERBOSE_PRINT.value,
                )
                gs.gui_service.quick_gui(
                    f"{track} is not one of the available files in the server tools media directory.",
                    text_type="header",
                    box_align="left",
                    user=data_actor["name"],
                )
                return

        st_settings.user_connections[username] = track
        st_utility.save_user_connections()
        if self.metadata.getboolean(
            C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False
        ):
            gs.gui_service.quick_gui(
                f"Set {track} to play whenever {username} connects to the server.",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
        else:
            gs.gui_service.quick_gui(
                f"Set {track} to play whenever {username} connects to the server,"
                f"<br>however the bot isn't configured to play audio clips when a user joins."
                f"<br>This feature can be enabled in the {self.plugin_name} metadata.ini file."
                f"<br>For a list of available sound clips, use '{get_command_token()}sblist'",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
        log(
            INFO,
            f"Set user connection sound: {track} to play whenever {username} connects to the server.",
            origin=L_COMMAND,
            print_mode=PrintMode.VERBOSE_PRINT.value,
        )

    def cmd_getloginsound(self, data):
        all_data = data.message.strip().split(" ", 1)
        data_actor = gs.mumble_inst.users[data.actor]
        if len(all_data) != 2:
            log(
                ERROR,
                CMD_INVALID_GET_USER_CONNECTION,
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                CMD_INVALID_GET_USER_CONNECTION,
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
            return

        username = all_data[1]
        st_utility.read_user_connections()
        if username not in st_settings.user_connections:
            log(
                ERROR,
                f"The provided username: {username} was not found in the user connections dictionary.",
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                f"The provided username was not found in the user connections dictionary."
                f"<br>You can add a new username to the dictionary with '{get_command_token()}setuserconnectionsound'",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
            return
        if not st_settings.user_connections[username]:
            log(
                ERROR,
                f"The provided username: {username} was found but an audio track was not assigned to the user connection.",
                origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR,
                print_mode=PrintMode.VERBOSE_PRINT.value,
            )
            gs.gui_service.quick_gui(
                f"The username was found but a sound clip was not assigned."
                f"<br>You can set a sound clip to the username with '{get_command_token()}setuserconnectionsound'"
                f"<br>For a list of available sound clips, use '{get_command_token()}sblist'",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
            return
        if self.metadata.getboolean(
            C_PLUGIN_SET, P_PLAY_AUDIO_CLIP_ON_USER_JOIN, fallback=False
        ):
            gs.gui_service.quick_gui(
                f"{st_settings.user_connections[username]} is set to play whenever {username} connects to the server.",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
        else:
            gs.gui_service.quick_gui(
                f"{st_settings.user_connections[username]} is set to play whenever {username} connects to the server,"
                f"<br>however the bot isn't configured to play audio clips when a user joins."
                f"<br>This feature can be enabled in the {self.plugin_name} metadata.ini file.",
                text_type="header",
                box_align="left",
                user=data_actor["name"],
            )
