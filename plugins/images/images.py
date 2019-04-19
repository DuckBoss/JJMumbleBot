from templates.plugin_template import PluginBase
from helpers.global_access import GlobalMods as GM
from helpers.global_access import debug_print, reg_print
import helpers.image_helper as IH
import utils
import os
import privileges as pv
from bs4 import BeautifulSoup
import time


class Plugin(PluginBase):
    help_data = "All commands can be run by typing it in the channel or privately messaging JJMumbleBot.<br>\
                        <b>!post 'image_url'</b>: Posts the image from the url in the channel chat.<br>\
                        <b>!img 'image_name'</b>: Posts locally hosted images in the channel chat. The image must be a jpg.<br>\
                        <b>!imglist</b>: Lists all locally hosted images."
    plugin_version = "1.8.3"
    priv_path = "images/images_privileges.csv"
    
    def __init__(self):
        debug_print("Images Plugin Initialized.")
        super().__init__()

    def process_command(self, mumble, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "post":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            img_url = message_parse[1]
            # Download image
            img_url = ''.join(BeautifulSoup(img_url, 'html.parser').findAll(text=True))
            IH.download_image_stream(img_url)
            # Format image
            time.sleep(1)
            img_ext = img_url.rsplit('.', 1)[1]
            formatted_string = IH.format_image("image", img_ext, utils.get_temporary_img_dir())

            # print(formatted_string)
            # print("%d characters" % len(formatted_string))
            reg_print("Posting an image to the mumble channel chat.")
            # utils.echo(utils.get_my_channel(mumble), formatted_string)
            GM.gui.quick_gui_img(f"{utils.get_temporary_img_dir()}", formatted_string, format=False)
            GM.logger.info(f"Posted an image to the mumble channel chat from: {message_parse[1]}.")
            return

        elif command == "img":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            parameter = message_parse[1]
            if not os.path.isfile(utils.get_permanent_media_dir()+f"images/{parameter}.jpg"):
                GM.gui.quick_gui(
                    "The image does not exist.",
                    text_type='header',
                    box_align='left')
                return False
            # Format image
            img_data = parameter.rsplit('.', 1)
            formatted_string = IH.format_image(img_data[0], "jpg", utils.get_permanent_media_dir()+"images/")
            reg_print("Posting an image to the mumble channel chat.")
            # utils.echo(utils.get_my_channel(mumble), formatted_string)
            GM.gui.quick_gui_img(f"{utils.get_permanent_media_dir()}images/", formatted_string, format=False)
            GM.logger.info("Posted an image to the mumble channel chat from local files.")
            return

        elif command == "imglist":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            file_counter = 0
            gather_list = []
            internal_list = []

            for file_item in os.listdir(utils.get_permanent_media_dir() + "images/"):
                if file_item.endswith(".jpg"):
                    gather_list.append(
                        f"{file_item}")
                    file_counter += 1

            gather_list.sort(key=str.lower)
            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>[{i}]</font> - [{item}]")

            cur_text = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Local Image Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local image files available."
                GM.gui.quick_gui(cur_text, text_type='header', box_align='left', user=mumble.users[text.actor]['name'])
                GM.logger.info("Displayed a list of all local image files.")
                return

            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    # utils.echo(utils.get_my_channel(mumble), cur_text)
                    GM.gui.quick_gui(cur_text, text_type='header', box_align='left', text_align='left', user=mumble.users[text.actor]['name'])
                    cur_text = ""
            # utils.echo(utils.get_my_channel(mumble), cur_text)
            if cur_text != "":
                GM.gui.quick_gui(cur_text, text_type='header', box_align='left', text_align='left', user=mumble.users[text.actor]['name'])
            GM.logger.info("Displayed a list of all local image files.")
            return

        elif command == "imglist_echo":
            if not pv.plugin_privilege_checker(mumble, text, command, self.priv_path):
                return
            file_counter = 0
            gather_list = []
            internal_list = []

            for file_item in os.listdir(utils.get_permanent_media_dir() + "images/"):
                if file_item.endswith(".jpg"):
                    gather_list.append(
                        f"{file_item}")
                    file_counter += 1

            gather_list.sort(key=str.lower)
            for i, item in enumerate(gather_list):
                internal_list.append(
                    f"<br><font color='{GM.cfg['PGUI_Settings']['IndexTextColor']}'>[{i}]</font> - [{item}]")

            cur_text = f"<font color='{GM.cfg['PGUI_Settings']['HeaderTextColor']}'>Local Image Files:</font>"
            if len(internal_list) == 0:
                cur_text += "<br>There are no local image files available."
                GM.gui.quick_gui(cur_text, text_type='header', box_align='left')
                GM.logger.info("Displayed a list of all local image files.")
                return

            for i, item in enumerate(internal_list):
                cur_text += item
                if i % 50 == 0 and i != 0:
                    # utils.echo(utils.get_my_channel(mumble), cur_text)
                    GM.gui.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
                    cur_text = ""
            # utils.echo(utils.get_my_channel(mumble), cur_text)
            if cur_text != "":
                GM.gui.quick_gui(cur_text, text_type='header', box_align='left', text_align='left')
            GM.logger.info("Displayed a list of all local image files.")
            return

    @staticmethod
    def plugin_test():
        debug_print("Images Plugin self-test callback.")

    def quit(self):
        debug_print("Exiting Images Plugin...")

    def help(self):
        return self.help_data

    def get_plugin_version(self):
        return self.plugin_version

    def get_priv_path(self):
        return self.priv_path

