from vrel.entity.Atom import Atom
from vrel.module.induction import ExplanationNode
from vrel.module.induction.GoalNode import GoalNode


class PlanNode(ExplanationNode):
    plan: Atom
    subepisodes: list[GoalNode]

    def __init__(self):
        super().__init__()
        self.subepisodes = []
