from vrel.core.constants import AUTO
from vrel.entity.Relation import Relation
from vrel.entity.Variable import Variable
from vrel.interface.SomeDataSource import SomeDataSource
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext


class SimpleModule(SomeModule):

    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("resolve_name", query_function=self.resolve_name))

    def resolve_name(self, arguments: list, context: ExecutionContext) -> list[list]:
        id = arguments[0]
        name = arguments[1].lower()

        out_values = self.ds.select("entity", ["id", "name"], [id, name])
        if len(out_values) > 0:
            return [[out_values[0][0], None]]
        else:
            self.ds.insert(
                "entity",
                [
                    "id",
                    "name",
                ],
                [AUTO if isinstance(id, Variable) else id, name],
            )

            out_values = self.ds.select("entity", ["id", "name"], [id, name])
            return [[out_values[0][0], None]]
