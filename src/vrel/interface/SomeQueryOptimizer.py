from abc import abstractmethod

from vrel.core.Model import Model
from vrel.entity.Atom import Atom


class SomeQueryOptimizer:
    @abstractmethod
    def optimize(
        self, composition: list[Atom], root_variables: list[str]
    ) -> tuple[str, list[Atom]]:
        pass
