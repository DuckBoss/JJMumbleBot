from JJMumbleBot.lib.privileges import Privileges, privileges_check,  plugin_privilege_checker
from JJMumbleBot.lib.resources.strings import P_THREAD_WAIT, P_THREAD_SINGLE, C_PLUGIN_SETTINGS, WARNING
from JJMumbleBot.settings import global_settings
from JJMumbleBot.lib.utils.logging_utils import log
from JJMumbleBot.lib.utils.runtime_utils import get_command_token
from JJMumbleBot.lib.utils.print_utils import PrintMode
from JJMumbleBot.lib.resources.strings import L_COMMAND, INFO
import threading
from json import loads


def execute_command(com):
    plugin = None

    # Check to see if the entered command has a registered callback.
    for command_clbk in global_settings.cmd_callbacks:
        if command_clbk == com.command:
            plugin = global_settings.bot_plugins[global_settings.cmd_callbacks[command_clbk][0]]
            break
    if not plugin:
        return

    # Check to make sure the plugin is initialized and running.
    if not plugin.is_running:
        log(WARNING, f"{plugin.plugin_name} has not implemented the 'is_running' attribute. "
                     "Commands from this plugin will be ignored!", print_mode=PrintMode.VERBOSE_PRINT.value)
        return

    # Check to make sure that WaitFor metadata is present in the plugin metadata.
    plugin_thr_settings = loads(plugin.metadata.get(C_PLUGIN_SETTINGS, P_THREAD_WAIT))
    if plugin_thr_settings is None:
        log(WARNING, "This plugin is missing the 'ThreadWaitForCommands' Tag in [Plugin Settings] "
                     "section in its metadata file.", print_mode=PrintMode.VERBOSE_PRINT.value)
        return
    use_single_thread = plugin.metadata.getboolean(C_PLUGIN_SETTINGS, P_THREAD_SINGLE, fallback=False)
    if use_single_thread is None:
        log(WARNING, "This plugin is missing the 'UseSingleThread' tag in [Plugin Settings] section "
                     "in its metadata file.", print_mode=PrintMode.VERBOSE_PRINT.value)
        return

    # Check user privileges before attempting to execute any commands.
    if privileges_check(com.text.actor) > Privileges.BLACKLIST.value:
        if not plugin_privilege_checker(com.text, com.command, plugin.plugin_name):
            global_settings.gui_service.quick_gui(
                f"{com.text.actor['name']} does not have the user privileges to use <code>{get_command_token()}{com.command}</code>.",
                text_type='header', box_align='left')
            log(INFO, f"{com.text.actor['name']} tried to use the {get_command_token()}{com.command} command, but lacked the user privileges to do so.",
            return
    else:
        global_settings.gui_service.quick_gui(
            f"Blacklisted user [{com.text.actor['name']}] does not have the user "
            f"privileges to use this command: [{com.command}]", text_type='header', box_align='left')
        log(INFO,
            f"{com.text.actor['name']} tried to use the {get_command_token()}{com.command} command, but is currently blacklisted.",
            origin=L_COMMAND, print_mode=PrintMode.VERBOSE_PRINT.value)
        return

    # Execute commands in either a blocking thread, or in a separate thread.
    if use_single_thread:
        global_settings.mtd_callbacks[f'{com.command}_clbk'](plugin, com.text)
        return
    thr = threading.Thread(target=global_settings.mtd_callbacks[f'{com.command}_clbk'], args=(plugin, com.text,))
    thr.start()
    if com.command in plugin_thr_settings:
        thr.join()
