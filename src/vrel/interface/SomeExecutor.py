from abc import ABC, abstractmethod

from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeSolver import SomeSolver


class SomeExecutor(ABC):

    @abstractmethod
    def process(self, product, solver: SomeSolver, request: SentenceRequest, logger: SomeLogger) -> ProcessResult:
        pass
