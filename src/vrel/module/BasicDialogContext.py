from vrel.core.constants import SAME_AS
from vrel.entity.Relation import Relation
from vrel.entity.Variable import Variable
from vrel.module.SqliteMemoryModule import SqliteMemoryModule
from vrel.entity.ExecutionContext import ExecutionContext


class BasicDialogContext(SqliteMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("context", formal_parameters=["name"]))

        self.add_relation(
            Relation("with_context", formal_parameters=["name", "body"], query_function=self.with_context)
        )
        self.add_relation(Relation("start_context", formal_parameters=["name"], query_function=self.start_context))
        self.add_relation(Relation("end_context", formal_parameters=["name"], query_function=self.end_context))
        self.add_relation(
            Relation(
                "same_as", formal_parameters=["id1", "id2"], query_function=self.same_as, write_function=self.write
            )
        )

    def with_context(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]
        body = arguments[1]
        self.data_source.insert("context", ["name"], [name])
        context.solver.solve(body)
        self.data_source.delete("context", ["name"], [name])
        return [[None, None]]

    def start_context(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]
        self.data_source.insert("context", ["name"], [name])
        return [[None]]

    def end_context(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]
        self.data_source.delete("context", ["name"], [name])
        return [[None]]

    def same_as(self, arguments: list, context: ExecutionContext) -> list[list]:
        term1, term2 = arguments

        if isinstance(term1, Variable) and isinstance(term2, Variable):
            return self.data_source.select(SAME_AS, ["id1", "id2"], [term1, term2])

        handler = context.solver.get_same_as_handler()
        if handler and handler.same_as(term1, term2):
            return [[None, None]]
        else:
            return []

    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE context (name TEXT)")
        cursor.execute("CREATE TABLE same_as (id1 TEXT, id2 TEXT)")
