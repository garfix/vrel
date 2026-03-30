from vrel.data_source.SimpleFrameDataSource import SimpleFrameDataSource
from vrel.entity.Relation import Relation
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext


class SimpleModule(SomeModule):

    data_source: SimpleFrameDataSource

    def __init__(self, data_source: SimpleFrameDataSource) -> None:
        super().__init__()
        self.data_source = data_source

        self.add_relation(Relation("goal", query_function=self.query, write_function=self.write))

    def query(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.data_source.select(context.relation.predicate, context.relation.formal_parameters, arguments)

    def write(self, arguments: list, context: ExecutionContext):
        self.data_source.insert(context.relation.predicate, context.relation.formal_parameters, arguments)
