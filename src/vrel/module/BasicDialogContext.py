import json

from vrel.core.constants import SAME_AS
from vrel.entity.Atom import Atom
from vrel.entity.Id import Id
from vrel.entity.Relation import Parameter, Relation
from vrel.entity.Variable import Variable
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
        self.add_relation(
            Relation(
                SAME_AS,
                parameters=[Parameter("id1", None), Parameter("id2", None)],
                query_function=self.same_as_read,
                write_function=self.same_as_write,
            )
        )

    def with_context(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]
        body = arguments[1]
        relation = self.get_relation("context")
        self.data_source.insert(relation, ["name"], [name])
        context.solver.solve(body)
        self.data_source.delete(relation, ["name"], [name])
        return [[None, None]]

    def start_context(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]
        context = self.get_relation("context")
        self.data_source.insert(context, ["name"], [name])
        return [[None]]

    def end_context(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[0]
        context = self.get_relation("context")
        self.data_source.delete(context, ["name"], [name])
        return [[None]]

    def same_as_read(self, arguments: list, context: ExecutionContext) -> list[list]:
        term1, term2 = arguments

        if isinstance(term1, Variable) and isinstance(term2, Variable):
            same_as = self.get_relation(SAME_AS)
            results = self.data_source.select(same_as, ["id1", "id2"], [term1, term2])

            # hydrated = [[json.loads(e) for e in result] for result in results]
            hydrated = []
            for result in results:
                row = []
                for e in result:
                    data = json.loads(e)
                    row.append(Id(data["id"], data["type"]))
                hydrated.append(row)

            return hydrated

        handler = context.model.get_same_as_handler()
        if handler and handler.same_as(term1, term2):
            return [[None, None]]
        else:
            return []

    def same_as_write(self, arguments: list, context: ExecutionContext) -> list[list]:

        dehydrated = [json.dumps({"id": id.id, "type": id.type}) for id in arguments]
        return self.write(dehydrated, context)

    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE context (name TEXT)")
        cursor.execute("CREATE TABLE same_as (entity_type TEXT, id1 TEXT, id2 TEXT)")
