from dataclasses import dataclass

from vrel.entity.Atom import Atom


@dataclass(frozen=True)
class SemanticFunction:
    args: list
    body: list[Atom]
