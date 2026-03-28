from abc import ABC, abstractmethod
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeLogger import SomeLogger


class SomeSystem(ABC):
    @abstractmethod
    def enter(self, request: SentenceRequest):
        pass

    @abstractmethod
    def read_output(self):
        pass
