import csv
from JJMumbleBot.lib.utils import dir_utils
from JJMumbleBot.lib.utils.print_utils import dprint, rprint
from JJMumbleBot.settings import global_settings as GS

users = {}
announcement = 'None'


def setup_statuses():
    with open(f"{dir_utils.get_main_dir()}/plugins/extensions/status/resources/status.csv", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        dprint("Setting up user statuses...")
        for i, row in enumerate(csvr):
            users[row['user']] = row['status']
            GS.log_service.info(f"Added [{row['user']}-{row['status']}] to the user status list.")


def status_check(username):
    if username in users.keys():
        return users[username]
    with open(f"{dir_utils.get_main_dir()}/plugins/extensions/status/resources/status.csv", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        for i, row in enumerate(csvr):
            if row['user'] == username:
                users[username] = row['status']
                return users[username]
    if username in (x['name'] for x in GS.mumble_inst.users.values()):
        with open(f"{dir_utils.get_main_dir()}/plugins/extensions/status/resources/status.csv", mode='a', newline='') as csvf:
            headers = ['user', 'status']
            csvw = csv.DictWriter(csvf, fieldnames=headers)
            csvw.writerow({'user': username, 'status': "None"})
            users[username] = "None"
            dprint(f"Added [{username}-{users[username]}] to the user status list.")
        return users[username]
    return None


def set_status(username, val):
    if username in users.keys():
        with open(f"{dir_utils.get_main_dir()}/plugins/extensions/status/resources/status.csv", mode='r') as csvf:
            csvr = csv.reader(csvf)
            content = list(csvr)
            ind = [(i, j.index(username)) for i, j in enumerate(content) if username in j]
            content[ind[0][0]][1] = val
            users[username] = val
            return overwrite_statuses(content)
    else:
        return False


def clear_status(username):
    if username in users.keys():
        with open(f"{dir_utils.get_main_dir()}/plugins/extensions/status/resources/status.csv", mode='r') as csvf:
            csvr = csv.reader(csvf)
            content = list(csvr)
            ind = [(i, j.index(username)) for i, j in enumerate(content) if username in j]
            content[ind[0][0]][1] = "None"
            users[username] = "None"
            return overwrite_statuses(content)
    else:
        return False


def add_to_status(username, status):
    with open(f"{dir_utils.get_main_dir()}/plugins/extensions/status/resources/status.csv", mode='a', newline='') as csvf:
        headers = ['user', 'status']
        csvw = csv.DictWriter(csvf, fieldnames=headers)
        csvw.writerow({'user': username, 'status': status})
        users[username] = status
        dprint(f"Added [{username}-{status}] to the status list.")
        return True


# TODO: Modify generic exception to a specific one.
def overwrite_statuses(content):
    try:
        with open(f"{dir_utils.get_main_dir()}/plugins/extensions/status/resources/status.csv", mode='w', newline='') as csvf:
            csvr = csv.writer(csvf)
            csvr.writerows(content)
            return True
    except Exception:
        dprint("There was a problem overwriting the status csv file.")
        GS.log_service.warning("There was a problem overwriting the status csv file.")
        return False
