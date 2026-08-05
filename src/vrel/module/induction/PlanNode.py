from typing import TYPE_CHECKING
from vrel.entity.Atom import Atom
from vrel.module.induction.ExplanationNode import ExplanationNode
from vrel.module.induction.GoalNode import GoalNode

if TYPE_CHECKING:
    from vrel.module.induction.GoalNode import GoalNode
    from vrel.module.induction.ActionNode import ActionNode


class PlanNode(ExplanationNode):
    plan: Atom
    subepisodes: list["GoalNode"]
    actions: list["ActionNode"]

    def __init__(self, id: int, plan: Atom):
        super().__init__(id)
        self.plan = plan
        self.subepisodes = []
        self.actions = []

    def get_atom(self) -> Atom:
        return self.plan

    def add_subepisode(self, child_id: int):
        self.subepisodes.append(child_id)

    def add_action(self, child_id: int):
        self.actions.append(child_id)

    def is_empty(self):
        return self.plan.predicate == "plan" and self.plan.arguments[0] == "variable"

    def get_subepisodes(self) -> list[int]:
        return self.subepisodes

    def get_actions(self) -> list[int]:
        return self.actions

    def __repr__(self):
        return f"Plan{self.plan}\n subepisodes: {self.subepisodes}\n actions: {self.actions}"
