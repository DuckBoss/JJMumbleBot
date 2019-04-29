from templates.plugin_template import PluginBase
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print
from plugins.sound_board.sound_board_helper import SoundBoardHelper as SBH
from plugins.youtube.youtube_helper import YoutubeHelper as YH
import plugins.sound_board.sound_board_helper as SBM
import utils
import privileges as pv
import os
from bs4 import BeautifulSoup


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
                    <b>!sb 'file_name'</b>: The file must be in wav format.<br>\
                    <b>!sbv '0..1'</b>: Sets the sound board audio volume.<br>\
                    <b>!sbreplay/!sbr</b>: Replays the last played sound board track.<br>\
                    <b>!sblist/!sbl</b>: Displays all the available sound board tracks in private messages.<br>\
                    <b>!sblist_echo/!sble</b> Displays all the available sound board tracks in the channel chat.<br>\
                    <b>!sbstop/!sbs</b>: Stops the currently playing sound board track.<br>\
                    <b>!sbdownload 'youtube_url' 'file_name'</b>: Downloads a sound clip from a youtube link and adds it to the sound board.<br>\
                    <b>!sbdelete 'file_name.wav'</b>: Deletes a clip from the sound board storage. Be sure to specify the .wav extension."
    plugin_version = "2.0.1"
    priv_path = "sound_board/sound_board_privileges.csv"

    youtube_plugin = None

    def __init__(self):
        debug_print("Sound_Board Plugin Initialized...")
        super().__init__()
        SBH.volume = float(GM.cfg['Plugin_Settings']['SoundBoard_DefaultVolume'])

    def set_youtube_plugin(self, yt_plugin):
        self.youtube_plugin = yt_plugin

    def process_command(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]
        if command == "sbstop":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if SBH.audio_thread is not None:
                SBM.stop_audio()
                GM.gui.quick_gui("Stopping sound board audio thread...", text_type='header', box_align='left')
                return
            return

        elif command == "sblist":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            file_counter = 0
            gather_list = []
            internal_list = []
            for file_item in os.listdir(utils.get_permanent_media_dir() + "sound_board/"):
                if file_item.endswith(".wav"):
                    gather_list.append(f"{file_item}")
                    file_counter += 1

            gather_list.sort(key=str.lower)
            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>[{i}]</font> - [{item}]")

            cur_text = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Local Sound Board Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local sound board files available."
                GM.gui.quick_gui(cur_text, text_type='header', box_align='left',
                                 user=GM.mumble.users[text.actor]['name'])
                GM.logger.info("Displayed a list of all local sound board files.")
                return

            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    GM.gui.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                     user=GM.mumble.users[text.actor]['name'])
                    cur_text = ""
            if cur_text != "":
                GM.gui.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                 user=GM.mumble.users[text.actor]['name'])
            GM.logger.info("Displayed a list of all local sound board files.")
            return

        elif command == "sblist_echo":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            file_counter = 0
            gather_list = []
            internal_list = []

            for file_item in os.listdir(utils.get_permanent_media_dir() + "sound_board/"):
                if file_item.endswith(".wav"):
                    gather_list.append(f"{file_item}")
                    file_counter += 1

            gather_list.sort(key=str.lower)
            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>[{i}]</font> - [{item}]")

            cur_text = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Local Sound Board Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local sound board files available."
                GM.gui.quick_gui(cur_text, text_type='header', box_align='left')
                GM.logger.info("Displayed a list of all local sound board files.")
                return

            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    GM.gui.quick_gui(cur_text, text_type='header', box_align='center', text_align='left')
                    cur_text = ""
            if cur_text != "":
                GM.gui.quick_gui(cur_text, text_type='header', box_align='center', text_align='left')
            GM.logger.info("Displayed a list of all local sound board files.")
            return

        elif command == "sbreplay":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if YH.is_playing:
                GM.gui.quick_gui("The youtube audio plugin is currently live. "
                                 "Use !stop before using the sound board plugin.",
                                 text_type='header', box_align='left')
                return
            if SBH.current_song is not None:
                self.youtube_plugin.clear_audio_plugin()
                SBM.play_audio()
            else:
                GM.gui.quick_gui("There is no sound board track available to replay.",
                                 text_type='header', box_align='left')
                return
            return

        elif command == "sbv":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                vol = float(message[1:].split(' ', 1)[1])
            except IndexError:
                GM.gui.quick_gui(f"Current sound board volume: {SBH.volume}", text_type='header',
                                 box_align='left')
                return
            if vol > 1:
                GM.gui.quick_gui("Invalid sound_board volume Input: [0-1]", text_type='header',
                                 box_align='left')
                return
            if vol < 0:
                GM.gui.quick_gui("Invalid sound_board volume Input: [0-1]", text_type='header',
                                 box_align='left')
                return
            SBH.volume = vol
            GM.gui.quick_gui(f"Set sound_board volume to {SBH.volume}", text_type='header',
                             box_align='left')
            return

        elif command == "sbdownload":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            all_messages_stripped = BeautifulSoup(message_parse[1], features='html.parser').get_text()
            split_msgs = all_messages_stripped.split()
            stripped_url = split_msgs[0]
            if len(all_messages) >= 3:
                if "youtube.com" in stripped_url or "youtu.be" in stripped_url:
                    SBM.download_clip(stripped_url, split_msgs[1].strip())
                    GM.gui.quick_gui(f"Downloaded sound clip as : {split_msgs[1].strip()}.wav", text_type='header',
                                     box_align='left')
                    return
                return
            return

        elif command == "sbdelete":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            if len(all_messages) == 2:
                if ".wav" in all_messages[1].strip():
                    utils.remove_file(all_messages[1].strip(), utils.get_permanent_media_dir() + "sound_board/")
                    GM.gui.quick_gui(f"Deleted sound clip : {all_messages[1].strip()}", text_type='header',
                                     box_align='left')

        elif command == "sb":
            if not pv.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameter = message_parse[1]

            if self.youtube_plugin.clear_audio_plugin() is False:
                GM.gui.quick_gui("The youtube audio plugin is currently live. "
                                 "Use !stop before using the sound board plugin.", text_type='header',
                                 box_align='left')
                return

            if not os.path.isfile(utils.get_permanent_media_dir() + f"sound_board/{parameter}.wav"):
                GM.gui.quick_gui(
                    "The sound clip does not exist.",
                    text_type='header',
                    box_align='left')
                return False
            SBH.current_song = parameter
            SBM.play_audio()

    def clear_audio_thread(self):
        if SBH.audio_thread is not None:
            debug_print("Clearing sound_board audio thread...")
            SBH.audio_thread.terminate()
            SBH.audio_thread.kill()
            SBH.audio_thread = None
            return True
        return False

    def plugin_test(self):
        debug_print("Sound_Board Plugin self-test callback.")

    def quit(self):
        self.clear_audio_thread()
        SBM.stop_audio()
        SBH.exit_flag = True
        debug_print("Exiting Sound_Board Plugin...")

    def help(self):
        return self.help_data

    def is_audio_plugin(self):
        return True

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path
