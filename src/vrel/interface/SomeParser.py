from abc import abstractmethod

from vrel.entity.ProcessResult import ProcessResult
from vrel.interface.SomeLogger import SomeLogger


class SomeParser:

    @abstractmethod
    def process(self, input: str, logger: SomeLogger) -> ProcessResult:
        pass
