from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import runtime_settings as RS
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.database_management_utils import get_memory_db
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.plugins.core.core_commands.resources.strings import *
from JJMumbleBot.plugins.core.core_commands.utility import core_commands_utility as cutils
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.privileges import Privileges, set_command_privileges, get_command_privileges
from JJMumbleBot.lib import aliases
from time import sleep
from bs4 import BeautifulSoup


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

    def cmd_stopplugin(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_STOP_PLUGIN,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_STOP_PLUGIN,
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        if cutils.turn_off_plugin(all_data[1]):
            GS.gui_service.quick_gui(
                f"Successfully stopped plugin: {all_data[1]}",
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        GS.gui_service.quick_gui(
            f"The plugin: {all_data[1]} could not be stopped.",
            text_type='header',
            box_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name'])

    def cmd_restartplugin(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_RESTART_PLUGIN,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_RESTART_PLUGIN,
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        if cutils.restart_plugin(all_data[1]):
            GS.gui_service.quick_gui(
                f"Successfully restarted plugin: {all_data[1]}",
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        GS.gui_service.quick_gui(
            f"The plugin: {all_data[1]} could not be restarted.",
            text_type='header',
            box_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name'])

    def cmd_startplugin(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_START_PLUGIN,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_START_PLUGIN,
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        if cutils.turn_on_plugin(all_data[1]):
            GS.gui_service.quick_gui(
                f"Successfully started plugin: {all_data[1]}",
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        GS.gui_service.quick_gui(
            f"The plugin: {all_data[1]} could not be started.",
            text_type='header',
            box_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name'])

    def cmd_sleep(self, data):
        sleep_time = float(data.message.strip().split(' ', 1)[1])
        RS.tick_rate = sleep_time
        log(INFO, f"Sleeping thread for {sleep_time}...", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        sleep(sleep_time)
        RS.tick_rate = float(GS.cfg[C_MAIN_SETTINGS][P_CMD_TICK_RATE])

    def cmd_version(self, data):
        GS.gui_service.quick_gui(
            f"{rutils.get_bot_name()} is on version {rutils.get_version()}",
            text_type='header',
            box_align='left'
        )

    def cmd_about(self, data):
        GS.gui_service.quick_gui(
            f"{rutils.get_about()}<br>{rutils.get_bot_name()} is on version {rutils.get_version()}",
            text_type='header',
            box_align='left'
        )

    def cmd_uptime(self, data):
        GS.gui_service.quick_gui(
            f"Up-time: {rutils.check_up_time()}",
            text_type='header',
            box_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name']
        )

    def cmd_exit(self, data):
        log(WARNING, "Stopping all threads...", origin=L_SHUTDOWN, print_mode=PrintMode.VERBOSE_PRINT.value)
        rutils.exit_bot()
        log(INFO, f"{rutils.get_bot_name()} is being shut down.", origin=L_SHUTDOWN, print_mode=PrintMode.VERBOSE_PRINT.value)
        log(INFO, "######################################", origin=L_GENERAL, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_restart(self, data):
        from os import execv
        from sys import argv, executable
        rutils.exit_bot()
        log(INFO, f"{rutils.get_bot_name()} is being restarted.", origin=L_STARTUP, print_mode=PrintMode.VERBOSE_PRINT.value)
        execv(executable, ['python3'] + argv)

    def cmd_saferestart(self, data):
        from os import execv
        from sys import argv, executable
        rutils.exit_bot()
        log(INFO, f"{rutils.get_bot_name()} is being rebooted in safe mode.", origin=L_STARTUP, print_mode=PrintMode.VERBOSE_PRINT.value)
        execv(executable, ['python3'] + argv + ['-safe'])

    def cmd_restartplugins(self, data):
        log(INFO, "Restarting Plugins", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        rutils.refresh_plugins()

    def cmd_setcomment(self, data):
        from JJMumbleBot.lib.utils.dir_utils import get_main_dir
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_SET_COMMENT,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_SET_COMMENT,
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        new_comment = all_data[1]
        # Set the new comment.
        GS.mumble_inst.users.myself.comment(
            f'{new_comment}<br><br>[{META_NAME}({META_VERSION})] - {rutils.get_bot_name()}<br>{rutils.get_about()}')
        # Write the new comment into the config file.
        GS.cfg.set(C_CONNECTION_SETTINGS, P_USER_COMMENT, new_comment)
        with open(f'{get_main_dir()}/cfg/config.ini', mode='w') as cfg_file:
            GS.cfg.write(cfg_file)

        GS.gui_service.quick_gui(
            f"Changed the bot's user comment.",
            text_type='header',
            box_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name'])
        log(INFO, f"Changed the bot's user comment to: {new_comment}.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_resetcomment(self, data):
        from JJMumbleBot.lib.utils.dir_utils import get_main_dir
        # Set the new comment.
        GS.mumble_inst.users.myself.comment(
            f'[{META_NAME}({META_VERSION})] - {rutils.get_bot_name()}<br>{rutils.get_about()}')
        # Write the new comment into the config file.
        GS.cfg.set(C_CONNECTION_SETTINGS, P_USER_COMMENT, "")
        with open(f'{get_main_dir()}/cfg/config.ini', mode='w') as cfg_file:
            GS.cfg.write(cfg_file)

        GS.gui_service.quick_gui(
            f"Reset the bot's user comment.",
            text_type='header',
            box_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name'])
        log(INFO, f"Reset the bot's user comment.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_pguistresstest(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) < 2:
            num_of_lines = 5
        else:
            num_of_lines = int(all_data[1])

        import random
        bg_colors = ["Blue", "Cyan", "Magenta", "Red", "Yellow", "Green", "Lime", "Black", "Snow", "Violet",
                     "Salmon", "Purple", "Pink", "Navy", "MintCream", "Maroon", "Gray", "Indigo", "Coral",
                     "Ivory", "Gold", "DodgerBlue", "CadetBlue", "Brown", "Beige", "Aquamarine"]
        GS.gui_service.open_box()

        for x in range(num_of_lines):
            content = GS.gui_service.make_content(
                f'<font color="{random.choice(bg_colors)}">[{x}] - PGUI STRESS TEST</font>',
                text_type='header',
                text_align="left",
                bgcolor=random.choice(bg_colors)
            )
            GS.gui_service.append_row(content)
            random.seed(x)

        GS.gui_service.close_box()
        GS.gui_service.display_box(channel=rutils.get_my_channel())
        log(INFO, f"Conducted PGUI stress test in the channel.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_help(self, data):
        all_data = data.message.strip().split()
        if len(all_data) < 2:
            all_plugin_names = [plugin for plugin in list(GS.bot_plugins)]
            all_plugin_metadata = [{"name": plugin_name, "metadata": GS.bot_plugins[plugin_name].metadata} for
                                   plugin_name in all_plugin_names]
            all_core_plugin_names = [(plugin_info["name"], plugin_info["metadata"][C_PLUGIN_INFO][P_PLUGIN_NAME]) for
                                     plugin_info in all_plugin_metadata if
                                     plugin_info["metadata"].getboolean(C_PLUGIN_TYPE, P_CORE_PLUGIN)]
            all_extension_plugin_names = [(plugin_info["name"], plugin_info["metadata"][C_PLUGIN_INFO][P_PLUGIN_NAME])
                                          for plugin_info in all_plugin_metadata if
                                          plugin_info["metadata"].getboolean(C_PLUGIN_TYPE, P_EXT_PLUGIN)]

            GS.gui_service.open_box()
            content = GS.gui_service.make_content(
                f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}">##### </font>'
                f'<b>{rutils.get_bot_name()} General Help Commands</b>'
                f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}"> #####</font>')
            GS.gui_service.append_row(content)

            content = GS.gui_service.make_content(
                f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}">##### </font>'
                f'<b>Core Plugins</b>'
                f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}"> #####</font>')
            GS.gui_service.append_row(content)
            for x, plugin_info in enumerate(all_core_plugin_names):
                content = GS.gui_service.make_content(
                    f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}">!help {plugin_info[0].strip()}</font> - Displays help information for the <font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}">{plugin_info[1]}</font> plugin.',
                    text_type='header',
                    text_align="left")
                GS.gui_service.append_row(content)

            content = GS.gui_service.make_content(
                f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}">##### </font>'
                f'<b>Extension Plugins</b>'
                f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}"> #####</font>')
            GS.gui_service.append_row(content)
            for x, plugin_info in enumerate(all_extension_plugin_names):
                content = GS.gui_service.make_content(
                    f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}">!help {plugin_info[0].strip()}</font> - Displays help information for the <font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}">{plugin_info[1].strip()}</font> plugin.',
                    text_type='header',
                    text_align="left")
                GS.gui_service.append_row(content)

            GS.gui_service.close_box()
            GS.gui_service.display_box(channel=rutils.get_my_channel())
            log(INFO, f"Displayed general help screen in the channel.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
            return

        plugin_name = all_data[1]
        plugin_help_data = PluginUtilityService.process_help(db_cursor=get_memory_db().cursor(),
                                                             plugin_name=plugin_name)
        if plugin_help_data:
            plugin_metadata = GS.bot_plugins[plugin_name].metadata

            GS.gui_service.open_box()
            all_help_lines = [msg.strip() for msg in plugin_help_data.split('<br>')]
            content = GS.gui_service.make_content(f'<font color="red">##### </font>'
                                                  f'<b>{rutils.get_bot_name()} Help Commands - [{plugin_name}]</b>'
                                                  f'<font color="red"> #####</font>')
            GS.gui_service.append_row(content)
            content = GS.gui_service.make_content(
                f'Plugin Version: {plugin_metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]}<br>', text_color='cyan')
            GS.gui_service.append_row(content)
            for x, help_item in enumerate(all_help_lines):
                item_parts = help_item.rsplit(':', 1)
                if len(item_parts) > 1:
                    content = GS.gui_service.make_content(
                        f'<font color="yellow">{item_parts[0]}</font>:{item_parts[1]}',
                        text_type='header',
                        text_align="left")
                else:
                    content = GS.gui_service.make_content(
                        f'{help_item}',
                        text_type='header',
                        text_align="left")
                GS.gui_service.append_row(content)
            GS.gui_service.close_box()
            GS.gui_service.display_box(channel=rutils.get_my_channel())
            log(INFO, f"Displayed help screen for {plugin_name} in the channel.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_importuserprivileges(self, data):
        from requests import get, HTTPError
        from JJMumbleBot.lib.utils.dir_utils import get_main_dir
        from JJMumbleBot.lib.privileges import import_user_privileges
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_IMPORT_PRIVILEGES,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_IMPORT_PRIVILEGES,
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        url = all_data[1].strip()
        if rutils.validate_url(url):
            try:
                resp = get(url)
                with open(f"{get_main_dir()}/cfg/downloads/{T_TEMP_USER_PRIVILEGES}.csv", "wb") as fileHandle:
                    fileHandle.write(resp.content)
                field_names = ["user", "level"]
                if not rutils.validate_csv(f"{get_main_dir()}/cfg/downloads/{T_TEMP_USER_PRIVILEGES}.csv", field_names):
                    GS.gui_service.quick_gui(
                        f"The downloaded csv file does not match the required format: {field_names}",
                        text_type='header',
                        text_align='left',
                        box_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name'])
                    return
                if import_user_privileges():
                    GS.gui_service.quick_gui(
                        f"Updated user privileges from the imported permission file!",
                        text_type='header',
                        text_align='left',
                        box_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name'])
                else:
                    GS.gui_service.quick_gui(
                        f"Encountered an error updating the user privileges from the imported user privileges file!",
                        text_type='header',
                        text_align='left',
                        box_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name'])
            except HTTPError:
                GS.gui_service.quick_gui(
                    f"An error occurred retrieving the user privileges file from the URL!",
                    text_type='header',
                    text_align='left',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[data.actor]['name'])
        else:
            GS.gui_service.quick_gui(
                f"Invalid URL provided!",
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])

    def cmd_importpermissions(self, data):
        from requests import get, HTTPError
        from JJMumbleBot.lib.utils.dir_utils import get_main_dir
        from JJMumbleBot.lib.privileges import import_command_permissions
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_IMPORT_PERMISSIONS,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_IMPORT_PERMISSIONS,
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        url = all_data[1].strip()
        if rutils.validate_url(url):
            try:
                resp = get(url)
                with open(f"{get_main_dir()}/cfg/downloads/{T_TEMP_CMD_PERMISSIONS}.csv", "wb") as fileHandle:
                    fileHandle.write(resp.content)
                field_names = ["command", "level"]
                if not rutils.validate_csv(f"{get_main_dir()}/cfg/downloads/{T_TEMP_USER_PRIVILEGES}.csv", field_names):
                    GS.gui_service.quick_gui(
                        f"The downloaded csv file does not match the required format: {field_names}",
                        text_type='header',
                        text_align='left',
                        box_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name'])
                    return
                if import_command_permissions():
                    GS.gui_service.quick_gui(
                        f"Updated command permissions from the imported permission file!",
                        text_type='header',
                        text_align='left',
                        box_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name'])
                else:
                    GS.gui_service.quick_gui(
                        f"Encountered an error updating the command permissions from the imported permission file!",
                        text_type='header',
                        text_align='left',
                        box_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name'])
            except HTTPError:
                GS.gui_service.quick_gui(
                    f"An error occurred retrieving the permissions file from the URL!",
                    text_type='header',
                    text_align='left',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[data.actor]['name'])
        else:
            GS.gui_service.quick_gui(
                f"Invalid URL provided!",
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])

    def cmd_getpermission(self, data):
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_GET_CMD_PERMISSION,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_GET_CMD_PERMISSION,
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        cmd_name = all_data[1].strip()
        cmd_data = get_command_privileges(cmd_name)
        if cmd_data:
            GS.gui_service.quick_gui(
                f"Command: {cmd_data['name']}<br>"
                f"Permission Level:{Privileges(int(cmd_data['level'])).name} ({cmd_data['level']})",
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
        else:
            GS.gui_service.quick_gui(
                f"Error retrieving command information for: {cmd_name}",
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])

    def cmd_changepermission(self, data):
        all_data = data.message.strip().split(' ', 2)
        if len(all_data) != 3:
            log(ERROR, CMD_INVALID_SET_CMD_PERMISSION,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_SET_CMD_PERMISSION,
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return

        cmd_name = all_data[1].strip()
        try:
            permission_level = int(all_data[2])
        except ValueError:
            log(ERROR, CMD_INVALID_SET_CMD_PERMISSION,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_SET_CMD_PERMISSION,
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        if permission_level <= Privileges.BLACKLIST.value or permission_level > Privileges.SUPERUSER.value:
            log(ERROR, CMD_INVALID_SET_CMD_PERMISSION_RANGE,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_SET_CMD_PERMISSION_RANGE,
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        if set_command_privileges(cmd_name=cmd_name, level=permission_level):
            GS.gui_service.quick_gui(
                f"Updated command permission level: [{cmd_name}] - [{Privileges(permission_level).name} ({permission_level})]",
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
        else:
            log(ERROR, "ERROR: An error occurred while modifying the command permission!",
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                "ERROR: An error occurred while modifying the command permission!",
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])

    def cmd_importaliases(self, data):
        from requests import get, HTTPError
        from JJMumbleBot.lib.utils.dir_utils import get_main_dir
        from JJMumbleBot.lib.aliases import import_aliases
        all_data = data.message.strip().split(' ', 1)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_IMPORT_ALIASES,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_IMPORT_ALIASES,
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        url = all_data[1].strip()
        if rutils.validate_url(url):
            try:
                resp = get(url)
                with open(f"{get_main_dir()}/cfg/downloads/{T_TEMP_ALIASES}.csv", "wb") as fileHandle:
                    fileHandle.write(resp.content)
                field_names = ["alias", "command"]
                if not rutils.validate_csv(f"{get_main_dir()}/cfg/downloads/{T_TEMP_USER_PRIVILEGES}.csv", field_names):
                    GS.gui_service.quick_gui(
                        f"The downloaded csv file does not match the required format: {field_names}",
                        text_type='header',
                        text_align='left',
                        box_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name'])
                    return
                if import_aliases():
                    GS.gui_service.quick_gui(
                        f"Updated aliases from the imported aliases file!",
                        text_type='header',
                        text_align='left',
                        box_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name'])
                else:
                    GS.gui_service.quick_gui(
                        f"Encountered an error updating the aliases from the imported aliases file!",
                        text_type='header',
                        text_align='left',
                        box_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name'])
            except HTTPError:
                GS.gui_service.quick_gui(
                    f"An error occurred retrieving the aliases file from the URL!",
                    text_type='header',
                    text_align='left',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[data.actor]['name'])
        else:
            GS.gui_service.quick_gui(
                f"Invalid URL provided!",
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])

    def cmd_setalias(self, data):
        all_data = data.message.strip().split(' ', 2)
        if len(all_data) < 3:
            log(ERROR, CMD_INVALID_SET_ALIAS,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                f"Incorrect Formatting!<br>"
                f"<font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Single Command Alias Example:</font> <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>(command)</font> parameters<br>"
                f"<font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Multi-Command Alias Example:</font> <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>(command)</font> parameters <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>|</font> <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>(command)</font> parameters ...",
                text_type='header',
                text_align='left',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
            return
        alias_name = all_data[1]

        all_coms = all_data[2].split('|')
        for com in all_coms:
            com_parse = com.split()[0]
            if com_parse[0] != '(' and com_parse[-1] != ')':
                log(INFO,
                    f'Could not register [{alias_name}] due to incorrect formatting.',
                    origin=L_ALIASES, print_mode=PrintMode.VERBOSE_PRINT.value)
                GS.gui_service.quick_gui(
                    f"<font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}>Could not register</font> [{alias_name}] <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}>due to incorrect formatting.</font><br>"
                    f"<font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Single Command Alias Example:</font> <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>(command)</font> parameters<br>"
                    f"<font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Multi-Command Alias Example:</font> <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>(command)</font> parameters <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>|</font> <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>(command)</font> parameters ...",
                    text_type='header',
                    text_align='left',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[data.actor]['name'])
                return
        if aliases.add_to_aliases(alias_name, all_data[2]):
            GS.gui_service.quick_gui(
                f"<font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Registered new alias:</font> <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>[{alias_name}]</font> - [{all_data[2]}]",
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
        elif aliases.set_alias(alias_name, all_data[2]):
            GS.gui_service.quick_gui(
                f"<font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>Registered alias:</font> <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_SUBHEAD_COL]}>[{alias_name}]</font> - [{all_data[2]}]",
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])

    def cmd_aliases(self, data):
        aliases_list = aliases.get_all_aliases()
        if len(aliases_list) == 0:
            cur_alias_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Registered Aliases: None</font>"
        else:
            cur_alias_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Registered Aliases:</font>"
            for i, alias in enumerate(aliases_list):
                cur_alias_text += f"<br><font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{alias[0]}]</font> - " \
                            f"[{BeautifulSoup(alias[1], 'html.parser').get_text()}] "
                if i % 50 == 0 and i != 0:
                    GS.gui_service.quick_gui(
                        cur_alias_text,
                        text_type='header',
                        box_align='left',
                        text_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[data.actor]['name']
                    )
                    cur_alias_text = ""
        GS.gui_service.quick_gui(
            cur_alias_text,
            text_type='header',
            box_align='left',
            text_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name']
        )
        log(INFO, "Displayed all registered aliases.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_removealias(self, data):
        all_data = data.message.strip().split(' ', 2)
        if len(all_data) != 2:
            log(ERROR, CMD_INVALID_REMOVE_ALIAS,
                origin=L_COMMAND, error_type=CMD_INVALID_ERR, print_mode=PrintMode.VERBOSE_PRINT.value)
            GS.gui_service.quick_gui(
                CMD_INVALID_REMOVE_ALIAS,
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name']
            )
            return
        alias_name = all_data[1]
        if aliases.remove_from_aliases(alias_name):
            GS.gui_service.quick_gui(
                f'Removed <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{alias_name}]</font> from registered aliases.',
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name']
            )
        else:
            GS.gui_service.quick_gui(
                f'Could not remove <font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{alias_name}]</font> from registered aliases.',
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name']
            )

    def cmd_clearaliases(self, data):
        if aliases.clear_aliases():
            GS.gui_service.quick_gui(
                'Cleared all registered aliases.',
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name']
            )
        else:
            GS.gui_service.quick_gui(
                'The registered aliases could not be cleared.',
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name']
            )

    def cmd_clearhistory(self, data):
        rutils.clear_command_history()
        GS.gui_service.quick_gui(
            f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}">Cleared command history.</font>',
            text_type='header',
            box_align='left',
            text_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name']
        )
        log(INFO, "Cleared command history.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)

    def cmd_history(self, data):
        cur_hist_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Command History:</font>"
        for i, item in enumerate(rutils.get_command_history()):
            cur_hist_text += f"<br><font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{i}]</font> - {item}"
            if i % 50 == 0 and i != 0:
                GS.gui_service.quick_gui(
                    cur_hist_text,
                    text_type='header',
                    box_align='left',
                    text_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[data.actor]['name']
                )
                cur_text = ""
        GS.gui_service.quick_gui(
            cur_hist_text,
            text_type='header',
            box_align='left',
            text_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name']
        )
        log(INFO, "Displayed command history.", origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
