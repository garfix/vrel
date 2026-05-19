from dataclasses import dataclass
from vrel.core.Logger import Logger
from vrel.entity.Atom import Atom
from vrel.interface.SomeProduct import SomeProduct


@dataclass
class AtomExecutorProduct(SomeProduct):
    bindings: list[dict]

    def get_output(self) -> any:
        return self.bindings
