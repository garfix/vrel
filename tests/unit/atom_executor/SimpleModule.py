from vrel.entity.Atom import Atom
from vrel.entity.Relation import Relation
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext


class SimpleModule(SomeModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("resolve_name", query_function=self.resolve_name))

    def resolve_name(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0].lower()

        context.solver.solve(
            [Atom("store", [Atom("output_type", "name_not_found"), Atom("output_name_not_found", name)])]
        )
        return []
