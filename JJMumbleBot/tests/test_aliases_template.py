from csv import DictReader
from JJMumbleBot.lib.utils.dir_utils import get_main_dir


class TestAliasesTemplate:
    def setup_method(self):
        self.alias_file_name = f"{get_main_dir()}/templates/aliases_template.csv"
        self.aliases_dict = {}
        try:
            with open(self.alias_file_name, mode='r') as csv_file:
                csvr = DictReader(csv_file)
                for i, row in enumerate(csvr):
                    self.aliases_dict[row['alias'].strip()] = row['command'].strip()
        except IOError:
            print(f"Encountered an IO error reading the alias file: [{self.alias_file_name}] during unit tests.")

    def test_alias_quit(self):
        assert self.aliases_dict["quit"] == "(exit)"

    def test_alias_volume(self):
        assert self.aliases_dict["v"] == "(volume)"

    def test_alias_queue(self):
        assert self.aliases_dict["q"] == "(queue)"

    def test_alias_replay(self):
        assert self.aliases_dict["rp"] == "(replay)"

    def test_alias_skip(self):
        assert self.aliases_dict["skip"] == "(next)"
