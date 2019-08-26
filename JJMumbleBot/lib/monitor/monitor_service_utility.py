from JJMumbleBot.lib.monitor import monitor_data
import psutil


def check_cpu_percent():
    cpu_perc = psutil.cpu_percent()
    if cpu_perc != monitor_data.cpu_percent:
        monitor_data.cpu_percent = cpu_perc


def check_ram_percent():
    ram_perc = psutil.virtual_memory()[2]
    if ram_perc != monitor_data.ram_percent:
        monitor_data.ram_percent = ram_perc
