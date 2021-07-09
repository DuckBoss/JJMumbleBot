from csv import reader
from JJMumbleBot.lib.utils.dir_utils import get_main_dir


class TestAliasesTemplate:
    def setup_method(self):
        self.alias_file_name = f"{get_main_dir()}/templates/aliases_template.csv"
        self.alias_header_list = []
        try:
            with open(self.alias_file_name, mode='rb') as csv_file:
                csvr = reader(csv_file)
                self.alias_header_list = next(csvr)
        except IOError:
            print(f"Encountered an IO error reading the alias file: [{self.alias_file_name}] during unit tests.")

    def test_alias_fields(self):
        assert set(self.alias_header_list) == {"alias", "command"}

