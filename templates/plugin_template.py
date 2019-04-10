from abc import ABC, abstractmethod

class PluginBase(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def process_command(self, mumble, text):
        pass

    @abstractmethod
    def plugin_test(self):
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def help(self):
        return help_data

    @abstractmethod 
    def get_plugin_version(self):
        return plugin_version

    @abstractmethod
    def get_priv_path(self):
        return priv_path

    @property
    @abstractmethod
    def help_data(self):
        pass

    @property
    @abstractmethod
    def plugin_version(self):
        pass

    @property
    def priv_path(self):
        pass
