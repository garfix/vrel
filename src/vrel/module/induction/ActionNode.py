from vrel.entity.Atom import Atom
from vrel.module.induction.ExplanationNode import ExplanationNode


class ActionNode(ExplanationNode):
    action: Atom

    def __init__(self, id: int, event: Atom):
        super().__init__(id)
        self.action = event

    def get_atom(self) -> Atom:
        return self.action

    def __repr__(self):
        return f"Action{self.action}"
