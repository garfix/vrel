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

    def add_attempt(self, child_id: int):
        self.attempts.append(child_id)

    def get_subepisodes(self) -> list[int]:
        return self.attempts

    def get_first_attempt(self):
        if len(self.attempts) > 0:
            return self.attempts[0]
        else:
            return None

    def __repr__(self):
        return f"Goal {self.id} {self.goal}\n attempts: {self.attempts}"
