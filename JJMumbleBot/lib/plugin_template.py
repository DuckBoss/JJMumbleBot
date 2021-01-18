from abc import ABC, abstractmethod


class PluginBase(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def quit(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError

    @abstractmethod
    def start(self):
        raise NotImplementedError
