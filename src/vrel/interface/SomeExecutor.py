from abc import ABC, abstractmethod

from vrel.entity.ProcessResult import ProcessResult
from vrel.interface.SomeLogger import SomeLogger


class SomeExecutor(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def process(self, request, logger: SomeLogger) -> ProcessResult:
        pass
