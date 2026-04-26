from abc import abstractmethod

from vrel.entity.Relation import Relation


class SomeSameAs:

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_same_as_variants(self, bound_arguments: list, relation: Relation) -> list[list]:
        pass
