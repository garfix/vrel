from __future__ import annotations

from vrel.entity.Atom import Atom


class ExplanationNode:
    id: int
    parent: ExplanationNode | None

    def __init__(self, id: int):
        self.id = id
        self.parent = None

    def get_atom(self) -> Atom:
        raise Exception("Not implemented")

    def set_atom(self, atom: Atom):
        raise Exception("Not implemented")

    def get_subepisodes(self) -> list[int]:
        raise Exception("Not implemented")
