from __future__ import annotations

from vrel.entity.Atom import Atom


class ExplanationNode:
    parent: ExplanationNode | None

    def __init__(self):
        self.parent = None

    def get_atom(self) -> Atom:
        pass
