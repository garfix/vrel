from abc import ABC, abstractmethod

from vrel.entity.Relation import Relation
from vrel.interface.SomePronounHandler import SomePronounHandler
from vrel.interface.SomeSameAsHandler import SomeSameAsHandler
from vrel.interface.SomeStackOverflowHandler import SomeStackOverflowHandler
from vrel.processor.semantic_composer.helper.VariableGenerator import VariableGenerator


class SomeModel(ABC):
    """
    This class represents the generic part of the model.
    """

    @abstractmethod
    def find_relations(self, predicate: str) -> list[Relation]:
        pass

    @abstractmethod
    def get_same_as_handler(self) -> SomeSameAsHandler:
        pass

    @abstractmethod
    def get_stack_overflow_handler(self) -> SomeStackOverflowHandler:
        pass

    # @abstractmethod
    # def get_pronoun_handler(self) -> SomePronounHandler:
    #     pass

    @abstractmethod
    def get_dialog_constant_generator(self) -> VariableGenerator:
        pass
