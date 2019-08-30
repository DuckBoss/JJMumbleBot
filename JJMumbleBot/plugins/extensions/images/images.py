from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.images.resources.strings import *
from JJMumbleBot.lib.helpers import image_helper as IH
import os
from bs4 import BeautifulSoup
import time


class Plugin(PluginBase):
    def get_metadata(self):
        pass

    def __init__(self):
        super().__init__()
        import json
        raw_file = os.path.basename(__file__)
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{raw_file}')
        self.plugin_cmds = json.loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.priv_path = f'plugins/extensions/{raw_file.split(".")[0]}/privileges.csv'
        self.help_path = f'plugins/extensions/{raw_file.split(".")[0]}/help.html'
        dir_utils.make_directory(f'{GS.cfg[C_MEDIA_DIR][P_PERM_MEDIA_DIR]}/images/')
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "post":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            img_url = message_parse[1]
            # Download image
            img_url = ''.join(BeautifulSoup(img_url, 'html.parser').findAll(text=True))
            IH.download_image_stream(img_url)
            # Format image
            time.sleep(1)
            img_ext = img_url.rsplit('.', 1)[1]
            formatted_string = IH.format_image("_image", img_ext, f'{dir_utils.get_temp_med_dir()}/images')
            rprint("Posting an image to the mumble channel chat.")
            # Display image with PGUI system
            GS.gui_service.quick_gui_img(f"{dir_utils.get_temp_med_dir()}/images", formatted_string,
                                         bgcolor=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_COL],
                                         cellspacing=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_SIZE],
                                         format=False)
            GS.log_service.info(f"Posted an image to the mumble channel chat from: {message_parse[1]}.")
            dir_utils.remove_file("_image.jpg", f'{dir_utils.get_temp_med_dir()}/images')
            return

        elif command == "img":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            parameters = message_parse[1].rsplit(".", 1)
            try:
                if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/images/{parameters[0]}.{parameters[1]}"):
                    GS.gui_service.quick_gui(
                        "The image does not exist.",
                        text_type='header',
                        box_align='left')
                    return False
            except IndexError:
                return False
            # Format image
            formatted_string = IH.format_image(parameters[0], parameters[1], f"{dir_utils.get_perm_med_dir()}/images/")
            rprint("Posting an image to the mumble channel chat.")
            # Display image with PGUI system
            GS.gui_service.quick_gui_img(f"{dir_utils.get_perm_med_dir()}/images/", formatted_string,
                                         bgcolor=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_COL],
                                         cellspacing=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_SIZE],
                                         format=False)
            GS.log_service.info("Posted an image to the mumble channel chat from local files.")
            return

        elif command == "imglist":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            file_counter = 0
            gather_list = []
            internal_list = []

            for file_item in os.listdir(f"{dir_utils.get_perm_med_dir()}/images/"):
                if file_item.lower().endswith(".jpg") or file_item.lower().endswith(".png"):
                    gather_list.append(
                        f"{file_item}")
                    file_counter += 1

            gather_list.sort(key=str.lower)
            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")

            cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local Image Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local image files available."
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left',
                                         user=GS.mumble_inst.users[text.actor]['name'])
                GS.log_service.info("Displayed a list of all local image files.")
                return

            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                             user=GS.mumble_inst.users[text.actor]['name'])
                    cur_text = ""
            if cur_text != "":
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                         user=GS.mumble_inst.users[text.actor]['name'])
            GS.log_service.info("Displayed a list of all local image files.")
            return

        elif command == "imglist_echo":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            file_counter = 0
            gather_list = []
            internal_list = []

            for file_item in os.listdir(f"{dir_utils.get_perm_med_dir()}/images/"):
                if file_item.lower().endswith(".jpg") or file_item.lower().endswith(".png"):
                    gather_list.append(
                        f"{file_item}")
                    file_counter += 1

            gather_list.sort(key=str.lower)
            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")

            cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local Image Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local image files available."
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left')
                GS.log_service.info("Displayed a list of all local image files.")
                return

            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
                    cur_text = ""
            if cur_text != "":
                GS.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
            GS.log_service.info("Displayed a list of all local image files.")
            return

    def quit(self):
        dprint("Exiting Images Plugin...")
