from abc import ABC, abstractmethod


class PluginBase(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def quit(self):
        pass
