from vrel.entity.Atom import Atom
from vrel.module.induction.ExplanationNode import ExplanationNode


class EventNode(ExplanationNode):
    event: Atom

    def __init__(self, id: int, event: Atom):
        super().__init__(id)
        self.event = event

    def get_atom(self) -> Atom:
        return self.event

    def __repr__(self):
        return f"Event{self.event}"
