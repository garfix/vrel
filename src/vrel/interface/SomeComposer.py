from abc import ABC, abstractmethod

from vrel.entity.ProcessResult import ProcessResult
from vrel.interface.SomeLogger import SomeLogger


class SomeComposer(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def process(self, request, logger: SomeLogger) -> ProcessResult:
        pass
