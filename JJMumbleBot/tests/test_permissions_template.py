from csv import reader
from JJMumbleBot.lib.utils.dir_utils import get_main_dir


class TestPermissionTemplate:
    def setup_method(self):
        self.permissions_file_name = f"{get_main_dir()}/templates/permissions_template.csv"
        self.permissions_header_list = []
        try:
            with open(self.permissions_file_name, mode='rb') as csv_file:
                csvr = reader(csv_file)
                self.permissions_header_list = next(csvr)
        except IOError:
            print(f"Encountered an IO error reading the command permissions file: [{self.permissions_file_name}] during unit tests.")

    def test_permissions_fields(self):
        assert set(self.permissions_header_list) == {"command", "level"}

