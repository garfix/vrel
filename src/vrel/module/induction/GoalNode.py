from typing import TYPE_CHECKING
from vrel.entity.Atom import Atom
from vrel.module.induction.ExplanationNode import ExplanationNode

if TYPE_CHECKING:
    from vrel.module.induction.PlanNode import PlanNode


class GoalNode(ExplanationNode):
    goal: Atom
    attempts: list["PlanNode"]

    def __init__(self, goal: Atom):
        super().__init__()
        self.goal = goal
        self.attempts = []

    def get_atom(self) -> Atom:
        return self.goal
