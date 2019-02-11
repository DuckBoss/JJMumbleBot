from enum import Enum

blacklist_names = []
admin_names = []


class Privileges(Enum):
    NORMAL = 1
    BLACKLIST = 2
    ADMIN = 3
