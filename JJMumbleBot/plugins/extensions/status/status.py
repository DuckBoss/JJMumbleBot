from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.extensions.status.resources.strings import *
from JJMumbleBot.plugins.extensions.status.utility import status_helper
import os


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
        status_helper.setup_statuses()
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "setannouncement":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if int(self.metadata[C_PLUGIN_SETTINGS][P_ANNC_CHR_LIM]) < len(message_parse[1]):
                GS.gui_service.quick_gui(
                    f"The given announcement message was too long! [Character Limit: "
                    f"{self.metadata[C_PLUGIN_SETTINGS][P_ANNC_CHR_LIM]}]",
                    text_type='header', box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                    ignore_whisper=True)
                return
            status_helper.announcement = message_parse[1]
            GS.gui_service.quick_gui(
                f"<font color='cyan'>Set Announcement:</font><br><font color='yellow'>{message_parse[1]}</font>",
                text_type='header', box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                ignore_whisper=True)
            return

        if command == "announcement":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if status_helper.announcement is None:
                GS.gui_service.quick_gui(
                    f"<font color='cyan'>Announcement:</font> <font color='yellow'>No announcement available.</font>",
                    text_type='header',
                    box_align='left')
                return
            GS.gui_service.quick_gui(
                f"<font color='cyan'>Announcement:</font><br><font color='yellow'>{status_helper.announcement}</font>",
                text_type='header',
                box_align='left')
            return

        if command == "clearannouncement":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if status_helper.announcement:
                status_helper.announcement = "None"
                GS.gui_service.quick_gui(
                    f"Cleared current announcement.",
                    text_type='header',
                    box_align='left')
                return
            return

        if command == "setstatus":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if int(self.metadata[C_PLUGIN_SETTINGS][P_STATUS_CHR_LIM]) < len(message_parse[1]):
                GS.gui_service.quick_gui(
                    f"The given status message was too long! [Character Limit: "
                    f"{self.metadata[C_PLUGIN_SETTINGS][P_STATUS_CHR_LIM]}]",
                    text_type='header', box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                    ignore_whisper=True)
                return
            status_helper.status_check(GS.mumble_inst.users[text.actor]['name'])
            if status_helper.set_status(GS.mumble_inst.users[text.actor]['name'], message_parse[1]):
                GS.gui_service.quick_gui(
                    f"<font color='cyan'>Set Status:</font><br><font color='yellow'>{message_parse[1]}</font>",
                    text_type='header', box_align='left', user=GS.mumble_inst.users[text.actor]['name'],
                    ignore_whisper=True)
                return
            GS.gui_service.quick_gui("Incorrect parameters! Format: !setstatus 'message'",
                                     text_type='header', box_align='left')
            return

        elif command == "status":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            try:
                stat = status_helper.status_check(message_parse[1])
            except IndexError:
                GS.gui_service.quick_gui("Incorrect parameters! Format: !status 'username'",
                                         text_type='header', box_align='left')
                return
            if stat is None:
                GS.gui_service.quick_gui(
                    f"<font color='cyan'>{message_parse[1]} Status:</font> <font color='yellow'>No status available.</font>",
                    text_type='header',
                    box_align='left')
                return
            GS.gui_service.quick_gui(
                f"<font color='cyan'>{message_parse[1]} Status:</font><br><font color='yellow'>{stat}</font>",
                text_type='header',
                box_align='left')
            return

        elif command == "mystatus":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            stat = status_helper.status_check(GS.mumble_inst.users[text.actor]['name'])
            if stat is None:
                GS.gui_service.quick_gui(
                    f"<font color='cyan'>{GS.mumble_inst.users[text.actor]['name']} Status:</font> <font color='yellow'>No status available.</font>",
                    text_type='header',
                    box_align='left')
                return
            GS.gui_service.quick_gui(
                f"<font color='cyan'>{GS.mumble_inst.users[text.actor]['name']} Status:</font><br><font color='yellow'>{stat}</font>",
                text_type='header',
                box_align='left')
            return

        elif command == "clearstatus":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if status_helper.clear_status(GS.mumble_inst.users[text.actor]['name']):
                GS.gui_service.quick_gui(
                    f"Status Cleared.",
                    text_type='header',
                    box_align='left')

    def quit(self):
        dprint("Exiting Status Plugin")
