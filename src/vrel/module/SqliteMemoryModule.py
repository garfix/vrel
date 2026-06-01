import sqlite3
from vrel.data_source.Sqlite3DataSource import Sqlite3DataSource
from vrel.entity.Relation import Relation
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext


class SqliteMemoryModule(SomeModule):

    def __init__(self) -> None:
        super().__init__()
        self.clear()

    def clear(self):
        connection = sqlite3.connect(":memory:")
        self.data_source = Sqlite3DataSource(connection)

    def add_relation(self, relation: Relation):
        self.relations[relation.predicate] = relation
        if not relation.query_function:
            relation.query_function = self.query
        if not relation.write_function:
            relation.write_function = self.write

    def query(self, values: list, context: ExecutionContext) -> list[list]:
        return self.select(context.relation, context.relation.get_parameter_names(), values)

    def write(self, values: list, context: ExecutionContext):
        self.insert(context.relation, context.relation.get_parameter_names(), values)
