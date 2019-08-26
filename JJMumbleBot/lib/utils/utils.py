import JJMumbleBot.settings.global_settings as gs
from time import time
from datetime import timedelta
from JJMumbleBot.lib.utils.print_utils import rprint


# Calculates the bot service up-time.
def check_time():
    gs.seconds = time() - gs.start_seconds
    return f"Up-time: {str(timedelta(seconds=gs.seconds)).split('.')[0]}"


# Prints all the contents of the config file.
def debug_config():
    print("\n-------------------------------------------")
    print("Debug Configuration File:")
    for sect in gs.cfg.sections():
        print(f"[{sect}]")
        for (key, val) in gs.cfg.items(sect):
            print(f"{key}={val}")
    print("-------------------------------------------\n")


# A callback test that prints out the test outputs of all the registered plugins.
def plugin_callback_test():
    # Plugin Callback Tests
    rprint("######### Running plugin callback tests #########")
    for plugin in gs.bot_service.bot_plugins.values():
        plugin.plugin_test()
    rprint("######### Plugin callback tests complete #########")