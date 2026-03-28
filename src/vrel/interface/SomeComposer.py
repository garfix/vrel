from abc import ABC, abstractmethod

from vrel.entity.ProcessResult import ProcessResult


class SomeComposer(ABC):

    @abstractmethod
    def get_name(self) -> str:
        pass


    @abstractmethod
    def process(self, request) -> ProcessResult:
        pass

