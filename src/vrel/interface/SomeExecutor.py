from abc import ABC, abstractmethod

from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeSolver import SomeSolver
from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence


class SomeExecutor(ABC):

    @abstractmethod
    def process(
        self, sentence: SemanticSentence, solver: SomeSolver, request: SentenceRequest, logger: SomeLogger
    ) -> ProcessResult:
        pass
