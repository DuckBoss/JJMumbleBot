from abc import ABC, abstractmethod


class PluginBase(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def process(self, text):
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def get_metadata(self):
        pass




