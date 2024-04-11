from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        pass
