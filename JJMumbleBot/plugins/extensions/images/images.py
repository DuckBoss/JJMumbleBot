from JJMumbleBot.lib.helpers import image_helper as IH
from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.plugins.extensions.images.resources.strings import *
from JJMumbleBot.settings import global_settings as gs
from os import path, listdir
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from requests import exceptions


class Plugin(PluginBase):
    def __init__(self):
        super().__init__()
        from json import loads
        self.plugin_name = path.basename(__file__).rsplit('.')[0]
        self.metadata = PluginUtilityService.process_metadata(f'plugins/extensions/{self.plugin_name}')
        self.plugin_cmds = loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        dir_utils.make_directory(f'{gs.cfg[C_MEDIA_SETTINGS][P_PERM_MEDIA_DIR]}/{self.plugin_name}/')
        log(
            INFO,
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.",
            origin=L_STARTUP,
            print_mode=PrintMode.REG_PRINT.value
        )

    def quit(self):
        log(
            INFO,
            f"Exiting {self.plugin_name} plugin...",
            origin=L_SHUTDOWN,
            print_mode=PrintMode.REG_PRINT.value
        )

    def cmd_post(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_POST, origin=L_COMMAND,
                error_type=CMD_INVALID_ERR, gui_service=gs.gui_service, print_mode=PrintMode.DEBUG_PRINT.value)
            return

        # Download image from the provided URL.
        img_url = all_data[1].strip()
        img_url = BeautifulSoup(img_url, 'html.parser').get_text()
        try:
            # Download the image in 1024 byte chunks and save it as a temporary image.
            IH.download_image_stream(img_url)
        except exceptions.HTTPError:
            log(ERROR, GEN_HTTP_ERROR, origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR, gui_service=gs.gui_service, print_mode=PrintMode.DEBUG_PRINT.value)
            return
        except exceptions.InvalidSchema:
            log(ERROR, GEN_INVALID_SCHEMA_ERROR, origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR, gui_service=gs.gui_service, print_mode=PrintMode.DEBUG_PRINT.value)
            return
        except exceptions.RequestException:
            log(ERROR, GEN_REQUESTS_ERROR, origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR, gui_service=gs.gui_service, print_mode=PrintMode.DEBUG_PRINT.value)
            return

        # Format the retrieved image into the b64 variant for mumble usage.
        img_ext = img_url.rsplit('.', 1)[1]
        formatted_string = IH.format_image(T_TEMP_IMG_NAME, img_ext, f'{dir_utils.get_temp_med_dir()}/internal/images')
        # Display image with PGUI system and log the event.
        gs.gui_service.quick_gui_img(f"{dir_utils.get_temp_med_dir()}/internal/images", formatted_string,
                                     bgcolor=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_COL],
                                     cellspacing=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_SIZE],
                                     format_img=False)
        log(INFO, INFO_POSTED_IMAGE, origin=L_COMMAND, print_mode=PrintMode.DEBUG_PRINT.value)

    def cmd_imgsearch(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_POST, origin=L_COMMAND,
                error_type=CMD_INVALID_ERR, gui_service=gs.gui_service, print_mode=PrintMode.DEBUG_PRINT.value)
            return
        search_query = all_data[1].strip()

        # Fuzzy search the file_name provided and only show up to 10 results with at least an 80% match.
        img_list = [file_item for file_item in listdir(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/")]
        file_ratios = process.extract(search_query, img_list)
        match_list = []
        for file_item in file_ratios:
            if file_item[1] > 80 and len(match_list) < 10:
                match_list.append(file_item[0])

        # Format and display the search results
        match_str = f"Search Results for <font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>{search_query}</font>: "
        if len(match_list) > 0:
            for i, clip in enumerate(match_list):
                match_str += f"<br><font color={gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{i + 1}]</font> - {clip}"
        else:
            match_str += "None"
        log(INFO, INFO_SEARCH_RESULTS, origin=L_COMMAND, print_mode=PrintMode.DEBUG_PRINT.value)
        gs.gui_service.quick_gui(
            match_str,
            text_type='header',
            text_align='left',
            box_align='left'
        )

    def cmd_img(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_POST, origin=L_COMMAND,
                error_type=CMD_INVALID_ERR, gui_service=gs.gui_service, print_mode=PrintMode.DEBUG_PRINT.value)
            return
        parameters = all_data[1].rsplit(".", 1)

        # Check if the image exists in the permanent media directory.
        if not path.isfile(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/{parameters[0]}.{parameters[1]}"):
            log(ERROR, CMD_IMAGE_DNE, origin=L_COMMAND,
                error_type=CMD_PROCESS_ERR, gui_service=gs.gui_service, print_mode=PrintMode.DEBUG_PRINT.value)
            return

        # Format the image and display it with the PGUI system.
        formatted_string = IH.format_image(parameters[0], parameters[1],
                                           f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/")
        gs.gui_service.quick_gui_img(f"{dir_utils.get_perm_med_dir()}/{self.plugin_name}/", formatted_string,
                                     bgcolor=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_COL],
                                     cellspacing=self.metadata[C_PLUGIN_SETTINGS][P_FRAME_SIZE],
                                     format_img=False)
        log(INFO, INFO_POSTED_IMAGE, origin=L_COMMAND, print_mode=PrintMode.DEBUG_PRINT.value)

    def cmd_imglist(self, data):
        data_actor = gs.mumble_inst.users[data.actor]
        file_counter = 0
        gather_list = []
        internal_list = []

        # Gather all image files ending with .jpg or .png extensions into a list.
        for file_item in listdir(f"{dir_utils.get_perm_med_dir()}/images/"):
            if file_item.lower().endswith(".jpg") or file_item.lower().endswith(".png"):
                gather_list.append(
                    f"{file_item}")
                file_counter += 1
        # Display a message in the channel chat if the gathered image list is empty.
        if len(gather_list) == 0:
            gs.gui_service.quick_gui(
                f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>There are no local image files available.</font>",
                text_type='header',
                box_align='left',
                user=data_actor['name'])
            return
        # Sort the gathered images list.
        gather_list.sort(key=str.lower)
        # Create a list of the formatted text for each image file.
        for i, item in enumerate(gather_list):
            internal_list.append(
                f"<br><font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}'>[{i}]</font> - [{item}]"
            )

        # Display the list of local image files in sections of 50 files to avoid hitting the character limit per message.
        cur_text = f"<font color='{gs.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Local Image Files:</font>"
        for i, item in enumerate(internal_list):
            cur_text += item
            if i % 50 == 0 and i != 0:
                gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                         user=data_actor['name'])
                cur_text = ""
        if cur_text != "":
            gs.gui_service.quick_gui(cur_text, text_type='header', box_align='left', text_align='left',
                                     user=data_actor['name'])
        log(INFO, INFO_DISPLAYED_ALL, origin=L_COMMAND, print_mode=PrintMode.DEBUG_PRINT.value)
