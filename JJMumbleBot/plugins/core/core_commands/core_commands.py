from JJMumbleBot.lib.plugin_template import PluginBase
from JJMumbleBot.settings import global_settings as GS
from JJMumbleBot.lib.utils import runtime_utils as rutils
from JJMumbleBot.lib.enums import BotState
from JJMumbleBot.settings import runtime_settings as RS
from JJMumbleBot.lib import privileges
from JJMumbleBot.lib.utils.print_utils import rprint, dprint
from JJMumbleBot.lib.utils.plugin_utils import PluginUtilityService
from JJMumbleBot.lib.resources.strings import *
from JJMumbleBot.lib import aliases
from time import sleep
from bs4 import BeautifulSoup


class Plugin(PluginBase):
    def quit(self):
        dprint("Exiting Bot_Commands Plugin...")

    def get_metadata(self):
        return self.metadata

    def __init__(self):
        super().__init__()
        import os
        import json
        raw_file = os.path.basename(__file__)
        self.metadata = PluginUtilityService.process_metadata(f'plugins/core/{raw_file}')
        self.plugin_cmds = json.loads(self.metadata.get(C_PLUGIN_INFO, P_PLUGIN_CMDS))
        self.priv_path = f'plugins/core/{raw_file.split(".")[0]}/privileges.csv'
        self.help_path = f'plugins/core/{raw_file.split(".")[0]}/help.html'
        rprint(
            f"{self.metadata[C_PLUGIN_INFO][P_PLUGIN_NAME]} v{self.metadata[C_PLUGIN_INFO][P_PLUGIN_VERS]} Plugin Initialized.")

    def process(self, text):
        message = text.message.strip()
        message_parse = message[1:].split(' ', 1)
        all_messages = message[1:].split()
        command = message_parse[0]

        if command == "sleep":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            sleep_time = float(text.message[1:].split(' ', 1)[1].strip())
            RS.tick_rate = sleep_time
            sleep(sleep_time)
            RS.tick_rate = float(GS.cfg[C_MAIN_SETTINGS][P_CMD_TICK_RATE])
            return

        elif command == "version":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            GS.gui_service.quick_gui(
                f"{rutils.get_bot_name()} is on version {rutils.get_version()}",
                text_type='header',
                box_align='left'
            )
            return

        elif command == "about":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            GS.gui_service.quick_gui(
                f"{rutils.get_about()}<br>{rutils.get_bot_name()} is on version {rutils.get_version()}",
                text_type='header',
                box_align='left'
            )
            return

        elif command == "botstatus":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            GS.gui_service.quick_gui(
                f"{rutils.get_bot_name()} is {'Online' if rutils.get_status() == BotState.ONLINE else 'Offline'}.",
                text_type='header',
                box_align='left'
            )
            return

        elif command == "uptime":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            GS.gui_service.quick_gui(
                rutils.check_uptime(),
                text_type='header',
                box_align='left',
                ignore_whisper=True,
                user=GS.mumble_inst.users[text.actor]['name']
            )
            return

        elif command == "exit":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            dprint("Stopping all threads...")
            rutils.exit_bot()
            GS.log_service.info("JJ Mumble Bot is being shut down.")
            GS.log_service.info("######################################")
            return

        elif command == "reboot":
            import os
            import sys
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            rutils.exit_bot()
            GS.log_service.info("JJ Mumble Bot is being rebooted.")
            os.execv(sys.executable, ['python3'] + sys.argv)
            return

        elif command == "refresh":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            rutils.refresh_plugins()
            return

        if command == "alias":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            message = text.message.strip()
            message_parse = message[1:].split(' ', 2)
            alias_name = message_parse[1]

            if alias_name in aliases.aliases.keys():
                aliases.set_alias(alias_name, message_parse[2])
                dprint(f"Registered alias: [{alias_name}] - [{message_parse[2]}]")
                GS.gui_service.quick_gui(
                    f"Registered alias: [{alias_name}] - [{message_parse[2]}]",
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name'])
            else:
                aliases.add_to_aliases(alias_name, message_parse[2])
                dprint(f"Registered new alias: [{alias_name}] - [{message_parse[2]}]")
                GS.gui_service.quick_gui(
                    f"Registered alias: [{alias_name}] - [{message_parse[2]}]",
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name'])
            return

        elif command == "aliases":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if len(aliases.aliases.items()) == 0:
                cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Registered Aliases: None</font>"
            else:
                cur_text = f"<font color='{GS.cfg[C_PGUI_SETTINGS][P_TXT_HEAD_COL]}'>Registered Aliases:</font>"
                for i, alias in enumerate(aliases.aliases):
                    cur_text += f"<br><font color={GS.cfg[C_PGUI_SETTINGS][P_TXT_IND_COL]}>[{alias}]</font> - " \
                                f"[{BeautifulSoup(aliases.aliases[alias], 'html.parser').get_text()}] "
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
            return

        elif command == "removealias":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            message = text.message.strip()
            message_parse = message[1:].split(' ', 2)
            alias_name = message_parse[1]
            if aliases.remove_from_aliases(alias_name):
                dprint(f'Removed [{alias_name}] from registered aliases.')
                GS.gui_service.quick_gui(
                    f'Removed [{alias_name}] from registered aliases.',
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name']
                )
            else:
                dprint(f'Could not remove [{alias_name}] from registered aliases.')
                GS.gui_service.quick_gui(
                    f'Could not remove [{alias_name}] from registered aliases.',
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name']
                )
            return

        elif command == "clearaliases":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return
            if aliases.clear_aliases():
                dprint('Cleared all registered aliases.')
                GS.gui_service.quick_gui(
                    'Cleared all registered aliases.',
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name']
                )
            else:
                dprint('The registered aliases could not be cleared.')
                GS.gui_service.quick_gui(
                    'The registered aliases could not be cleared.',
                    text_type='header',
                    box_align='left',
                    ignore_whisper=True,
                    user=GS.mumble_inst.users[text.actor]['name']
                )
            return

        elif command == "clearhistory":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
                return

        elif command == "history":
            if not privileges.plugin_privilege_checker(text, command, self.priv_path):
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
