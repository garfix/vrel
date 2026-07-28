from vrel.entity.Atom import Atom
from vrel.module.induction.ExplanationNode import ExplanationNode


class EventNode(ExplanationNode):
    event: Atom

    def __init__(self, event: Atom):
        super().__init__()
        self.event = event

    def get_atom(self) -> Atom:
        return self.event
