from dataclasses import dataclass
from vrel.core.Logger import Logger
from vrel.entity.Atom import Atom
from vrel.interface.SomeProduct import SomeProduct


@dataclass
class AtomExecutorProduct(SomeProduct):
    bindings: list[dict]
    resolved: list[Atom]

    def log(self, logger: Logger):
        logger.add_subheader("Resolved")
        logger.add(str(self.resolved))
        logger.add_subheader("Result bindings")
        logger.add("\n".join(str(d) for d in self.bindings))

    def get_output(self) -> any:
        return self.bindings
