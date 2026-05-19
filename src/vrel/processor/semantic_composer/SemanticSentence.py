from dataclasses import dataclass
from vrel.core.Logger import Logger
from vrel.core.functions.terms import format_term
from vrel.entity.Atom import Atom


@dataclass(frozen=True)
class SemanticSentence:
    semantics: list[Atom]
    root_variables: list[str]
