from __future__ import annotations
from dataclasses import dataclass
from vrel.entity.PositionType import PositionType


class RuleConstituent:
    predicate: str
    arguments: list[str]
    position_type: PositionType
    optional: bool
    separator: bool
    hash: int
    function: str | None

    def __init__(
        self,
        predicate: str,
        arguments: list[str],
        position_type: PositionType,
        optional: bool = False,
        separator: bool = False,
        function: str | None = None,
    ):
        self.predicate = predicate
        self.arguments = arguments
        self.position_type = position_type
        self.optional = optional
        self.separator = separator
        self.function = function

        h = [c for c in arguments] + [self.predicate, self.position_type, self.function]
        self.hash = hash(tuple(h))

    def equals(self, other: RuleConstituent):
        if self.predicate != other.predicate:
            return False

        if len(self.arguments) != len(other.arguments):
            return False

        if self.position_type != other.position_type:
            return False

        return True

    def __str__(self) -> str:
        return (
            (self.function + ":" if self.function else "")
            + self.predicate
            + "("
            + ", ".join([argument for argument in self.arguments])
            + ")"
        )
