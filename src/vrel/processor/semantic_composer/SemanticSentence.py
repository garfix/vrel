from dataclasses import dataclass
from vrel.entity.Atom import Atom


@dataclass(frozen=True)
class SemanticSentence:
    semantics: list[Atom]
    root_variables: list[str]
