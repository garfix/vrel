from vrel.entity.Relation import Relation
from vrel.module.SqliteMemoryModule import SqliteMemoryModule


class AtomExecutorDialogContext(SqliteMemoryModule):

    def __init__(self) -> None:
        super().__init__()
        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE isa (entity TEXT, type TEXT)")
        cursor.execute("CREATE TABLE continent (entity TEXT)")
        cursor.execute("CREATE TABLE concept (type TEXT)")

        self.add_relation(Relation("isa", formal_parameters=["entity", "type"]))
        self.add_relation(Relation("continent", formal_parameters=["entity"]))
        self.add_relation(Relation("concept", formal_parameters=["type"]))
