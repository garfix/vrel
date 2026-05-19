from abc import ABC, abstractmethod

from vrel.entity.ParseTreeNode import ParseTreeNode
from vrel.entity.ProcessResult import ProcessResult
from vrel.interface.SomeLogger import SomeLogger


class SomeComposer(ABC):

    @abstractmethod
    def process(self, parse_trees: list[ParseTreeNode], logger: SomeLogger) -> ProcessResult:
        pass
