from JJMumbleBot.settings.global_settings import cfg, bot_service
from JJMumbleBot.lib.utils.print_utils import rprint, dprint


# Prints all the contents of the config file.
def debug_config():
    dprint("\n-------------------------------------------")
    dprint("Debug Configuration File:")
    for sect in cfg.sections():
        dprint(f"[{sect}]")
        for (key, val) in cfg.items(sect):
            dprint(f"{key}={val}")
    dprint("-------------------------------------------\n")


# A callback test that prints out the test outputs of all the registered plugins.
def plugin_callback_test():
    # Plugin Callback Tests
    rprint("######### Running plugin callback tests #########")
    for plugin in bot_service.bot_plugins.values():
        plugin.plugin_test()
    rprint("######### Plugin callback tests complete #########")