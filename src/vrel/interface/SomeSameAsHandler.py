from abc import abstractmethod

from vrel.entity.Id import Id
from vrel.entity.Relation import Relation


class SomeSameAsHandler:

    @abstractmethod
    def get_same_as_variants(self, bound_arguments: list, relation: Relation) -> list[list]:
        pass

    def get_same_as(self, id: Id) -> list[int | str]:
        pass

    def clear_cache(self):
        pass
