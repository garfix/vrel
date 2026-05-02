from abc import ABC, abstractmethod

from vrel.entity.Relation import Relation
from vrel.interface.SomeSameAsHandler import SomeSameAsHandler
from vrel.interface.SomeStackOverflowHandler import SomeStackOverflowHandler


class SomeModel(ABC):
    """
    This class represents the generic part of the model.
    """

    @abstractmethod
    def find_relations(self, predicate: str) -> list[Relation]:
        pass

    @abstractmethod
    def get_same_as_handler(self) -> SomeSameAsHandler | None:
        pass

    @abstractmethod
    def get_stack_overflow_handler(self) -> SomeStackOverflowHandler | None:
        pass
