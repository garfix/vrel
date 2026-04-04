from vrel.entity.Atom import Atom
from vrel.entity.InductionRule import InductionRule
from dataclasses import dataclass


@dataclass(frozen=True)
class Link:
    atoms: list[Atom]
    rules: list[InductionRule]
