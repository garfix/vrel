from __future__ import annotations


class ExplanationNode:
    parent: ExplanationNode | None

    def __init__(self):
        self.parent = None
