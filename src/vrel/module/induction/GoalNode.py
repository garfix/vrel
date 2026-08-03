from typing import TYPE_CHECKING
from vrel.entity.Atom import Atom
from vrel.module.induction.ExplanationNode import ExplanationNode

if TYPE_CHECKING:
    from vrel.module.induction.PlanNode import PlanNode


class GoalNode(ExplanationNode):
    goal: Atom
    attempts: list["PlanNode"]

    def __init__(self, id: int, goal: Atom):
        super().__init__(id)
        self.goal = goal
        self.attempts = []

    def get_atom(self) -> Atom:
        return self.goal

    def add_child(self, child_id: int):
        self.attempts.append(child_id)

    def get_children(self) -> list[int]:
        return self.attempts

    def __repr__(self):
        return f"Goal{self.goal}\n attempts: {self.attempts}"
