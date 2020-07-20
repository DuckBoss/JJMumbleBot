from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import runtime_settings as RS
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.utils.database_management_utils import get_memory_db
from JJMumbleBot.lib.resources.strings import *
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
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def quit(self):
        dprint(f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)
        log(INFO, f"Exiting {self.plugin_name} plugin...", origin=L_SHUTDOWN)

    def cmd_sleep(self, data):
        sleep_time = float(data.message.strip().split(' ', 1)[1])
        RS.tick_rate = sleep_time
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
        dprint("Stopping all threads...")
        rutils.exit_bot()
        log(INFO, "JJMumbleBot is being shut down.")
        log(INFO, "######################################")

    def cmd_restart(self, data):
        from os import execv
        from sys import argv, executable
        rutils.exit_bot()
        log(INFO, "JJMumbleBot is being restarted.", origin=L_STARTUP)
        execv(executable, ['python3'] + argv)

    def cmd_saferestart(self, data):
        from os import execv
        from sys import argv, executable
        rutils.exit_bot()
        log(INFO, "JJ Mumble Bot is being rebooted in safe mode.", origin=L_STARTUP)
        execv(executable, ['python3'] + argv + ['-safe'])  # nosec

    def cmd_restartplugins(self, data):
        rutils.refresh_plugins()

    def cmd_setcomment(self, data):
        from JJMumbleBot.lib.utils.dir_utils import get_main_dir
        all_data = data.message.strip().split(' ', 1)
        new_comment = all_data[1]
        if len(all_data) < 2:
            return
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
        dprint(f"Changed the bot\'s user comment to {new_comment}.")
        log(INFO, f"Changed the bot\'s user comment to {new_comment}.", origin=L_COMMAND)

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
        dprint(f"Reset the bot\'s user comment.")
        log(INFO, f"Reset the bot\'s user comment.", origin=L_COMMAND)

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
        dprint(f"Conducted PGUI stress test in the channel.")
        log(INFO, f"Conducted PGUI stress test in the channel.", origin=L_COMMAND)

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
            dprint(f"Displayed general help screen in the channel.")
            log(INFO, f"Displayed general help screen in the channel.", origin=L_COMMAND)
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
                item_parts = help_item.split(':', 1)
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
            dprint(f"Displayed help screen for {plugin_name} in the channel.")
            log(INFO, f"Displayed help screen for {plugin_name} in the channel.", origin=L_COMMAND)

    def cmd_setalias(self, data):
        all_data = data.message.strip().split(' ', 2)
        if len(all_data) < 2:
            return
        alias_name = all_data[1]

        if aliases.add_to_aliases(alias_name, all_data[2]):
            GS.gui_service.quick_gui(
                f"Registered new alias: [{alias_name}] - [{all_data[2]}]",
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name'])
        elif aliases.set_alias(alias_name, all_data[2]):
            GS.gui_service.quick_gui(
                f"Registered alias: [{alias_name}] - [{all_data[2]}]",
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

    def cmd_removealias(self, data):
        all_data = data.message.strip().split(' ', 2)
        if len(all_data) < 2:
            return
        alias_name = all_data[1]
        if aliases.remove_from_aliases(alias_name):
            GS.gui_service.quick_gui(
                f'Removed [{alias_name}] from registered aliases.',
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[data.actor]['name']
            )
        else:
            GS.gui_service.quick_gui(
                f'Could not remove [{alias_name}] from registered aliases.',
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
        GS.cmd_history.queue_storage.clear()
        GS.gui_service.quick_gui(
            f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}">Cleared command history.</font>',
            text_type='header',
            box_align='left',
            text_align='left',
            ignore_whisper=True,
            user=GS.mumble_inst.users[data.actor]['name']
        )

    def cmd_history(self, data):
        cur_hist_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Command History:</font>"
        for i, item in enumerate(GS.cmd_history.queue_storage):
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
