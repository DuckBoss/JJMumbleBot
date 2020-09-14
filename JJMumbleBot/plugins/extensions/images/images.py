import os

from bs4 import BeautifulSoup
from requests import exceptions

from JJMumbleBot.lib.helpers import image_helper as IH
from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.plugins.extensions.images.resources.strings import *
from JJMumbleBot.settings import global_settings as gs


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = os.path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def cmd_post(self, data):
        all_data = data.message.strip().split(' ', 1)
        img_url = all_data[1]
        # Download image
        img_url = BeautifulSoup(img_url, 'html.parser').get_text()
        try:
            IH.download_image_stream(img_url)
        except exceptions.HTTPError:
            gs.gui_service.quick_gui(
                "Encountered an HTTP Error while trying to retrieve the image.",
                text_type='header',
                text_align='left',
                box_align='left'
            )
            return
        except exceptions.InvalidSchema:
            gs.gui_service.quick_gui(
                "Encountered an Invalid Schema Error while trying to retrieve the image.",
                text_type='header',
                text_align='left',
                box_align='left'
            )
            return
        except exceptions.RequestException:
            gs.gui_service.quick_gui(
                "Encountered a Request Error while trying to retrieve the image.",
                text_type='header',
                text_align='left',
                box_align='left'
            )
            return
        img_ext = img_url.rsplit('.', 1)[1]
        formatted_string = IH.format_image("_image", img_ext, f'{dir_utils.get_temp_med_dir()}/internal/images')
        rprint("Posting an image to the mumble channel chat.")
        # Display image with PGUI system
        gs.gui_service.quick_gui_img(f"{dir_utils.get_temp_med_dir()}/internal/images", formatted_string,
                                     bgcolor=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_COL],
                                     cellspacing=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_SIZE],
                                     format_img=False)
        log(INFO, f"Posted an image to the mumble channel chat from: {img_url}.")

    def cmd_img(self, data):
        all_data = data.message.strip().split()
        parameters = all_data[1].rsplit(".", 1)
        try:
            if not os.path.isfile(f"{dir_utils.get_perm_med_dir()}/images/{parameters[0]}.{parameters[1]}"):
                gs.gui_service.quick_gui(
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
        gs.gui_service.quick_gui_img(f"{dir_utils.get_perm_med_dir()}/images/", formatted_string,
                                     bgcolor=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_COL],
                                     cellspacing=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_SIZE],
                                     format_img=False)
        log(INFO, "Posted an image to the mumble channel chat from local files.")

    def cmd_imglist(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
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
                f"<br><font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]")

        cur_text = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local Image Files:</font>"
        if len(internal_list) == 0:
            cur_text += "<br>There are no local image files available."
            gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left',
                                     user=data_actor['name'])
            gs.log_service.info("Displayed a list of all local image files.")
            return

        for i, item in enumerate(internal_list):
            cur_text += item
            if i % 50 == 0 and i != 0:
                gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                         user=data_actor['name'])
                cur_text = ""
        if cur_text != "":
            gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                     user=data_actor['name'])
        log(INFO, "Displayed a list of all local image files.")
