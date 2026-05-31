from vrel.entity.Atom import Atom
from vrel.entity.Relation import Parameter, Relation
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.module.optimizer.IsolateIndependentParts import IsolateIndependentParts
from vrel.module.optimizer.SortByCost import SortByCost


class OptimizerModule(SomeModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(
            Relation(
                "optimize_isolate",
                parameters=[Parameter("sem_in", list[Atom]), Parameter("sem_out", list[Atom])],
                query_function=self.optimize_isolate,
            )
        ),
        self.add_relation(
            Relation(
                "optimize_cost_sort",
                parameters=[Parameter("sem_in", list[Atom]), Parameter("sem_out", list[Atom])],
                query_function=self.optimize_cost_sort,
            )
        ),

    # ('optimize_isolate', SemIn, SemOut)
    # performs David H.D. Warren's optimization
    def optimize_isolate(self, arguments: list, context: ExecutionContext) -> list[list]:
        sem_in = arguments[0]
        sem_out = IsolateIndependentParts().isolate(sem_in, context.request.semantic_sentence.root_variables)
        return [[None, sem_out]]

    # ('optimize_cost_sort', SemIn, SemOut)
    # sorts atoms by decreasing cost
    def optimize_cost_sort(self, arguments: list, context: ExecutionContext) -> list[list]:
        sem_in = arguments[0]
        sem_out = SortByCost().sort(sem_in, context.solver, context.model)
        return [[None, sem_out]]
