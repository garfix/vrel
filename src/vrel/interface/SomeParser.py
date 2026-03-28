from abc import ABC, abstractmethod

from vrel.entity.ProcessResult import ProcessResult
from vrel.interface.SomeProcessor import SomeProcessor


class SomeParser(SomeProcessor):

    @abstractmethod
    def get_name(self) -> str:
        pass


    @abstractmethod
    def process(self, request) -> ProcessResult:
        pass

