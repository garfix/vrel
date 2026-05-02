from dataclasses import dataclass
from vrel.core.Logger import Logger
from vrel.core.functions.terms import format_term
from vrel.entity.Atom import Atom


@dataclass(frozen=True)
class SemanticSentence:
    semantics: list[Atom]
    root_variables: list[str]

    def log(self, logger: Logger):
        logger.add_subheader("Semantics")
        logger.add(format_term(self.semantics))
        logger.add_subheader("Inferences")
        logger.add_subheader("Return variables")
        logger.add(", ".join(self.root_variables))
