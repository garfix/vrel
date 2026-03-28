from vrel.data_source.SimpleFrameDataSource import SimpleFrameDataSource
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Relation import Relation
from vrel.interface.SomeModule import SomeModule


class PlanAnalyzerDialogContext(SomeModule):

    data_source: SimpleFrameDataSource

    def __init__(self) -> None:
        super().__init__()
        self.data_source = SimpleFrameDataSource()

        self.add_relation(Relation("same_as", formal_parameters=["mention_1", "mention_2"], query_function=self.query, write_function=self.write))


    def query(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.data_source.select(context.relation.predicate, context.relation.formal_parameters, arguments)


    def write(self, arguments: list, context: ExecutionContext):
        self.data_source.insert(context.relation.predicate, context.relation.formal_parameters, arguments)


    def clear(self):
        self.data_source.clear()

