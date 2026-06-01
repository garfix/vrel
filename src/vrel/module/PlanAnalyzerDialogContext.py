import json

from vrel.core.constants import SAME_AS
from vrel.data_source.SimpleFrameDataSource import SimpleFrameDataSource
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Relation import Parameter, Relation
from vrel.entity.Variable import Variable
from vrel.interface.SomeModule import SomeModule


class PlanAnalyzerDialogContext(SomeModule):

    def __init__(self) -> None:
        super().__init__()
        self.data_source = SimpleFrameDataSource()

        # self.add_relation(Relation("same_as", formal_parameters=["mention_1", "mention_2"], query_function=self.query, write_function=self.write))
        self.add_relation(
            Relation(
                SAME_AS,
                parameters=[Parameter("mention_1", None), Parameter("mention_2", None)],
                query_function=self.same_as_read,
                write_function=self.same_as_write,
            )
        )

    def same_as_read(self, arguments: list, context: ExecutionContext) -> list[list]:
        term1, term2 = arguments

        if isinstance(term1, Variable) and isinstance(term2, Variable):
            results = self.select(SAME_AS, ["id1", "id2"], [term1, term2])

            hydrated = [[json.loads(e) for e in result] for result in results]
            return hydrated

        handler = context.model.get_same_as_handler()
        if handler and handler.same_as(term1, term2):
            return [[None, None, None]]
        else:
            return []

    def same_as_write(self, arguments: list, context: ExecutionContext) -> list[list]:

        dehydrated = [[json.dumps(e) for e in argument] for argument in arguments]
        return self.write(dehydrated, context)

    def query(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.select(context.relation.predicate, context.relation.formal_parameters, arguments)

    def write(self, arguments: list, context: ExecutionContext):
        self.insert(context.relation.predicate, context.relation.formal_parameters, arguments)

    def clear(self):
        self.data_source.clear()
