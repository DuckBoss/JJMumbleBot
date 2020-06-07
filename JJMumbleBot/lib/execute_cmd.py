from JJMumbleBot.lib.resources.strings import P_THREAD_WAIT, P_THREAD_SINGLE, C_PLUGIN_SETTINGS, WARNING
from JJMumbleBot.lib.utils.logging_utils import log
import threading
from json import loads


def execute_command(plugin, com):
    plugin_thr_settings = loads(plugin.metadata.get(C_PLUGIN_SETTINGS, P_THREAD_WAIT))
    if plugin_thr_settings is None:
        log(WARNING, "This plugin is missing the 'ThreadWaitForCommands' Tag in [Plugin Settings] "
                                      "section in its metadata file.")
        return

    use_single_thread = plugin.metadata.getboolean(C_PLUGIN_SETTINGS, P_THREAD_SINGLE, fallback=False)
    if use_single_thread is None:
        log(WARNING, "This plugin is missing the 'UseSingleThread' tag in [Plugin Settings] section "
                                      "in its metadata file.")
        return
    if use_single_thread:
        plugin.process(com.text)
        return

    thr = threading.Thread(target=plugin.process, args=(com.text,))
    thr.start()
    if com.command in plugin_thr_settings:
        thr.join()
