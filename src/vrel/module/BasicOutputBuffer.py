from vrel.data_source.SimpleDataSource import SimpleDataSource
from vrel.entity.Relation import Parameter, Relation
from vrel.module.SqliteMemoryModule import SqliteMemoryModule


class BasicOutputBuffer(SqliteMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.add_relation(Relation("output_type", parameters=[Parameter("type")]))
        self.add_relation(Relation("output_value", parameters=[Parameter("value")]))
        self.add_relation(Relation("output_value_with_unit", parameters=[Parameter("value"), Parameter("unit")]))
        self.add_relation(Relation("output_table", parameters=[Parameter("results"), Parameter("units")]))
        self.add_relation(Relation("output_list", parameters=[Parameter("elements")]))
        self.add_relation(Relation("output_name_not_found", parameters=[Parameter("name")]))
        self.add_relation(Relation("output_unknown_word", parameters=[Parameter("word")]))

    def clear(self):
        self.data_source = SimpleDataSource()
