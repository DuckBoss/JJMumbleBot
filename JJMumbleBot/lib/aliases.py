import csv
from JJMumbleBot.lib.utils import dir_utils
import logging

aliases = {}
alias_path = "cfg/aliases.csv"


def setup_aliases_debug():
    with open(f"{dir_utils.get_main_dir()}/{alias_path}", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        print("Setting up registered aliases...")
        for i, row in enumerate(csvr):
            aliases[row['alias']] = row['command']
            print("Added [%s-%s] to the registered aliases list." % (row['alias'], row['command']))
            logging.info("Added [%s-%s] to the registered aliases list." % (row['alias'], row['command']))


def setup_aliases():
    with open(f"{dir_utils.get_main_dir()}/{alias_path}", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        print("Setting up registered aliases...")
        for i, row in enumerate(csvr):
            aliases[row['alias']] = row['command']
            logging.info("Added [%s-%s] to the registered aliases list." % (row['alias'], row['command']))


def alias_check(alias):
    if alias in aliases.keys():
        return aliases[alias]

    with open(f"{dir_utils.get_main_dir()}/{alias_path}", mode='r') as csvf:
        csvr = csv.DictReader(csvf)
        for i, row in enumerate(csvr):
            if row['alias'] == alias:
                aliases[alias] = row['command']
                return alias[alias]
    return None


def set_alias(alias, command):
    if alias in aliases.keys():
        with open(f"{dir_utils.get_main_dir()}/{alias_path}", mode='r') as csvf:
            csvr = csv.reader(csvf)
            content = list(csvr)
            ind = [(i, j.index(alias)) for i, j in enumerate(content) if alias in j]
            content[ind[0][0]][1] = command
            aliases[alias] = command
            return overwrite_aliases(content)
    return False


def remove_from_aliases(alias):
    if alias in aliases.keys():
        aliases.pop(alias, None)
        with open(f"{dir_utils.get_main_dir()}/{alias_path}", mode='r') as csvf:
            csvr = csv.reader(csvf)
            content = list(csvr)
            ind = [(i, j.index(alias)) for i, j in enumerate(content) if alias in j]
            if (content[ind[0][0]][0]) == alias:
                content.remove(content[ind[0][0]])
            return overwrite_aliases(content)


def clear_aliases():
    aliases.clear()
    with open(f"{dir_utils.get_main_dir()}/{alias_path}", mode='w') as csvf:
        fields = ['alias', 'command']
        csvw = csv.DictWriter(csvf, fieldnames=fields)
        csvw.writeheader()
        return True


def add_to_aliases(alias, command):
    with open(f"{dir_utils.get_main_dir()}/{alias_path}", mode='a', newline='') as csvf:
        headers = ['alias', 'command']
        csvw = csv.DictWriter(csvf, fieldnames=headers)
        csvw.writerow({'alias': alias, 'command': command})
        aliases[alias] = command
        print("Added [%s-%s] to the user list." % (alias, command))
        return True


def overwrite_aliases(content):
    try:
        with open(f"{dir_utils.get_main_dir()}/{alias_path}", mode='w', newline='') as csvf:
            csvw = csv.writer(csvf)
            csvw.writerows(content)
            return True
    except Exception:
        print("There was a problem overwriting the privileges csv file.")
        logging.critical("There was a problem overwriting the privileges csv file.")
        return False
