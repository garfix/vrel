from abc import abstractmethod

from vrel.entity.Atom import Atom


class SomeStackOverflowHandler:

    @abstractmethod
    def check_stack(self, atom: Atom) -> bool:
        pass

    @abstractmethod
    def remove(self, atom: Atom):
        pass
