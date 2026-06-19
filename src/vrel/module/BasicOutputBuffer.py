from vrel.data_source.SimpleDataSource import SimpleDataSource
from vrel.entity.Atom import Atom
from vrel.entity.Relation import Parameter, Relation
from vrel.module.SqliteMemoryModule import SqliteMemoryModule


class BasicOutputBuffer(SqliteMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.add_relation(Relation("output_type", parameters=[Parameter("type", str)]))
        self.add_relation(Relation("output_value", parameters=[Parameter("value", any)]))
        self.add_relation(
            Relation("output_value_with_unit", parameters=[Parameter("value", any), Parameter("unit", str)])
        )
        self.add_relation(
            Relation("output_table", parameters=[Parameter("results", list[any]), Parameter("units", list[str])])
        )
        self.add_relation(Relation("output_list", parameters=[Parameter("elements", list[any])]))
        self.add_relation(Relation("output_explanation", parameters=[Parameter("explanation", Atom)]))
        self.add_relation(Relation("output_name_not_found", parameters=[Parameter("name", str)]))
        self.add_relation(Relation("output_unknown_word", parameters=[Parameter("word", str)]))

    def clear(self):
        self.data_source = SimpleDataSource()
