from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.settings import runtime_settings as RS
from JJMumbleBot.lib import privileges
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

    def get_metadata(self):
        return self.metadata

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        command = message_parse[0]

        if command == "sleep":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            sleep_time = float(text.message[1:].split(' ', 1)[1].strip())
            RS.tick_rate = sleep_time
            sleep(sleep_time)
            RS.tick_rate = float(GS.cfg[C_MAIN_SETTINGS][P_CMD_TICK_RATE])

        elif command == "version":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.gui_service.quick_gui(
                f"{rutils.get_bot_name()} is on version {rutils.get_version()}",
                text_type='header',
                box_align='left'
            )

        elif command == "about":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.gui_service.quick_gui(
                f"{rutils.get_about()}<br>{rutils.get_bot_name()} is on version {rutils.get_version()}",
                text_type='header',
                box_align='left'
            )

        elif command == "uptime":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.gui_service.quick_gui(
                rutils.check_up_time(),
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[text.actor]['name']
            )

        elif command == "exit":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            dprint("Stopping all threads...")
            rutils.exit_bot()
            log(INFO, "JJ Mumble Bot is being shut down.")
            log(INFO, "######################################")

        elif command == "reboot":
            import os
            import sys
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            rutils.exit_bot()
            log(INFO, "JJ Mumble Bot is being rebooted.", origin=L_STARTUP)
            os.execv(sys.executable, ['python3'] + sys.argv) # nosec

        elif command == "safereboot":
            import os
            import sys
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            rutils.exit_bot()
            log(INFO, "JJ Mumble Bot is being rebooted in safe mode.", origin=L_STARTUP)
            os.execv(sys.executable, ['python3'] + sys.argv + ['-safe']) # nosec

        elif command == "refresh":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            rutils.refresh_plugins()

        elif command == "help":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            message = text.message.strip()
            message_parse = message[1:].split(' ', 2)
            if len(message_parse) < 2:
                return
            plugin_name = message_parse[1]

            plugin_help_data = PluginUtilityService.process_help(db_cursor=get_memory_db().cursor(), plugin_name=plugin_name)
            if plugin_help_data:
                plugin_metadata = GS.bot_plugins[plugin_name].metadata

                GS.gui_service.open_box()
                all_help_lines = [msg.strip() for msg in plugin_help_data.split('<br>')]
                content = GS.gui_service.make_content(f'<font color="red">##### </font>'
                                                      f'<b>{rutils.get_bot_name()} Help Commands - [{plugin_name}]</b>'
                                                      f'<font color="red"> #####</font>')
                GS.gui_service.append_row(content)
                content = GS.gui_service.make_content(f'Plugin Version: {plugin_metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]}<br>', text_color='cyan')
                GS.gui_service.append_row(content)
                for i, item in enumerate(all_help_lines):
                    item_parts = item.split(':', 1)
                    if len(item_parts) > 1:
                        content = GS.gui_service.make_content(
                            f'<font color="yellow">{item_parts[0]}</font>:{item_parts[1]}',
                            text_type='header',
                            text_align="left")
                    else:
                        content = GS.gui_service.make_content(
                            f'{item}',
                            text_type='header',
                            text_align="left")
                    GS.gui_service.append_row(content)
                GS.gui_service.close_box()
                GS.gui_service.display_box(channel=rutils.get_my_channel())
                dprint(f"Displayed help screen for {plugin_name} in the channel.")
                log(INFO, f"Displayed help screen for {plugin_name} in the channel.", origin=L_COMMAND)

        elif command == "alias":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            message = text.message.strip()
            message_parse = message[1:].split(' ', 2)
            if len(message_parse) < 2:
                return
            alias_name = message_parse[1]

            if aliases.add_to_aliases(alias_name, message_parse[2]):
                GS.gui_service.quick_gui(
                    f"Registered new alias: [{alias_name}] - [{message_parse[2]}]",
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name'])
            elif aliases.set_alias(alias_name, message_parse[2]):
                GS.gui_service.quick_gui(
                    f"Registered alias: [{alias_name}] - [{message_parse[2]}]",
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name'])

        elif command == "aliases":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            aliases_list = aliases.get_all_aliases()
            if len(aliases_list) == 0:
                cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Registered Aliases: None</font>"
            else:
                cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Registered Aliases:</font>"
                for i, alias in enumerate(aliases_list):
                    cur_text += f"<br><font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{alias[0]}]</font> - " \
                                f"[{BeautifulSoup(alias[1], 'html.parser').get_text()}] "
                    if i % 50 == 0 and i != 0:
                        GS.gui_service.quick_gui(
                            cur_text,
                            text_type='header',
                            box_align='left',
                            text_align='left',
                            ignore_whisper=True,
                            user=GS.mumble_inst.users[text.actor]['name']
                        )
                        cur_text = ""
            GS.gui_service.quick_gui(
                cur_text,
                text_type='header',
                box_align='left',
                text_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[text.actor]['name']
            )

        elif command == "removealias":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            message = text.message.strip()
            message_parse = message[1:].split(' ', 2)
            if len(message_parse) < 2:
                return
            alias_name = message_parse[1]
            if aliases.remove_from_aliases(alias_name):
                GS.gui_service.quick_gui(
                    f'Removed [{alias_name}] from registered aliases.',
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name']
                )
            else:
                GS.gui_service.quick_gui(
                    f'Could not remove [{alias_name}] from registered aliases.',
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name']
                )

        elif command == "clearaliases":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            if aliases.clear_aliases():
                GS.gui_service.quick_gui(
                    'Cleared all registered aliases.',
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name']
                )
            else:
                GS.gui_service.quick_gui(
                    'The registered aliases could not be cleared.',
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name']
                )

        elif command == "clearhistory":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            GS.cmd_history.queue_storage.clear()
            GS.gui_service.quick_gui(
                f'<font color="{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}">Cleared command history.</font>',
                text_type='header',
                box_align='left',
                text_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[text.actor]['name']
            )

        elif command == "history":
            if not privileges.plugin_privilege_checker(text, command, self.plugin_name):
                return
            cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Command History:</font>"
            for i, item in enumerate(GS.cmd_history.queue_storage):
                cur_text += f"<br><font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{i}]</font> - {item}"
                if i % 50 == 0 and i != 0:
                    GS.gui_service.quick_gui(
                        cur_text,
                        text_type='header',
                        box_align='left',
                        text_align='left',
                        ignore_whisper=True,
                        user=GS.mumble_inst.users[text.actor]['name']
                    )
                    cur_text = ""
            GS.gui_service.quick_gui(
                cur_text,
                text_type='header',
                box_align='left',
                text_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[text.actor]['name']
            )
