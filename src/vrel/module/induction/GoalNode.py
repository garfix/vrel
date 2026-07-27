from vrel.entity.Atom import Atom
from vrel.module.induction.ExplanationNode import ExplanationNode
from vrel.module.induction.PlanNode import PlanNode


class GoalNode(ExplanationNode):
    goal: Atom
    attempts: list[PlanNode]

    def __init__(self):
        super().__init__()
        self.attempts = []
