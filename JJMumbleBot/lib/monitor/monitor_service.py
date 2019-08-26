from JJMumbleBot.lib.monitor import monitor_service_utility as msu
from JJMumbleBot.settings import runtime_settings
import time


def loop_monitor_check():
    msu.check_cpu_percent()
    msu.check_ram_percent()
    # time.sleep(runtime_settings.tick_rate)

