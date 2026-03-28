from dataclasses import dataclass

from . import Variable


@dataclass(frozen=True)
class Atom:
    name: str
    variable: Variable


    def __str__(self) -> str:
        return str(self.name)


