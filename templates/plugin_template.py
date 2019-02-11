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
        pass
