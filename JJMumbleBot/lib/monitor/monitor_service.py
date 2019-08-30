from JJMumbleBot.lib.monitor import monitor_service_utility as msu


def monitor_check():
    msu.check_cpu_percent()
    msu.check_ram_percent()
