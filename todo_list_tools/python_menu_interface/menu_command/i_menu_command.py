# Menu Command
from abc import ABC, abstractmethod

class IMenuCommand(ABC):
    @abstractmethod
    def execute(self):
        pass
