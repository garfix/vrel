from vrel.entity.Atom import Atom
from vrel.entity.Relation import Parameter, Relation
from vrel.module.SqliteMemoryModule import SqliteMemoryModule
from vrel.entity.ExecutionContext import ExecutionContext


class BasicDialogContext(SqliteMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("context", parameters=[Parameter("name", str)]))

        self.add_relation(
            Relation(
                "with_context",
                parameters=[Parameter("name", str), Parameter("body", list[Atom])],
                query_function=self.with_context,
            )
        )
        self.add_relation(
            Relation("start_context", parameters=[Parameter("name", str)], query_function=self.start_context)
        )
        self.add_relation(Relation("end_context", parameters=[Parameter("name", str)], query_function=self.end_context))

    def with_context(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]
        body = arguments[1]
        relation = self.get_relation("context")
        self.insert(relation, ["name"], [name])
        context.solver.solve(body)
        self.delete(relation, ["name"], [name])
        return [[None, None]]

    def start_context(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]
        context = self.get_relation("context")
        self.insert(context, ["name"], [name])
        return [[None]]

    def end_context(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]
        context = self.get_relation("context")
        self.delete(context, ["name"], [name])
        return [[None]]

    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE context (name TEXT)")
