from csv import DictReader
from JJMumbleBot.lib.utils.dir_utils import get_main_dir


class TestPermissionTemplate:
    def setup_method(self):
        self.permissions_file_name = f"{get_main_dir()}/templates/permissions_template.csv"
        self.aliases_dict = {}
        try:
            with open(self.permissions_file_name, mode='r') as csv_file:
                csvr = DictReader(csv_file)
                for i, row in enumerate(csvr):
                    self.aliases_dict[row['command'].strip()] = row['level'].strip()
        except IOError:
            print(f"Encountered an IO error reading the command permissions file: [{self.permissions_file_name}] during unit tests.")

    def test_alias_fields(self):
        assert self.aliases_dict["command"] == "level"

