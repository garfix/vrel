from typing import TYPE_CHECKING
from vrel.entity.Atom import Atom
from vrel.module.induction.ExplanationNode import ExplanationNode
from vrel.module.induction.GoalNode import GoalNode

if TYPE_CHECKING:
    from vrel.module.induction.GoalNode import GoalNode


class PlanNode(ExplanationNode):
    plan: Atom
    subepisodes: list["GoalNode"]

    def __init__(self, plan: Atom):
        super().__init__()
        self.plan = plan
        self.subepisodes = []

    def get_atom(self) -> Atom:
        return self.plan
