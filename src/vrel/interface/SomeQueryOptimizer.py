from abc import abstractmethod

from vrel.core.Model import Model


class SomeQueryOptimizer:
    @abstractmethod
    def optimize(self, composition: list[tuple], root_variables: list[str]) -> tuple[str, list[tuple]]:
        pass
