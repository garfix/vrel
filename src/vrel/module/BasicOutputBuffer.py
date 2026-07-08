from vrel.core.functions.unification import unification
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Relation import Parameter, Relation
from vrel.interface.SomeModule import SomeModule


class BasicOutputBuffer(SomeModule):

    output: list

    def __init__(self) -> None:
        super().__init__()

        self.output = []

        self.add_relation(
            Relation(
                "out",
                parameters=[Parameter("type", str), Parameter("value", any), Parameter("value", any)],
                query_function=self.out,
            )
        )
        self.add_relation(
            Relation(
                "last_output",
                parameters=[Parameter("type", any), Parameter("value", any), Parameter("value", any)],
                query_function=self.last_output,
            )
        )
        self.add_relation(Relation("clear_output", parameters=[], query_function=self.clear_output))
        self.add_relation(Relation("any_output", parameters=[], query_function=self.any_output))

    def out(self, values: list, context: ExecutionContext) -> list[list]:
        self.output.append(values)
        return [values]

    def last_output(self, values: list, context: ExecutionContext) -> list[list]:
        if len(self.output) == 0:
            return []
        out = self.output[-1]
        if len(out) != len(values):
            return []
        if unification(out, values, {}) is not None:
            return [out]
        return []

    def clear_output(self, values: list, context: ExecutionContext) -> list[list]:
        self.output = []
        return [[]]

    def any_output(self, values: list, context: ExecutionContext) -> list[list]:
        if len(self.output) > 0:
            return [[]]
        else:
            return []

    def clear(self):
        self.output = []
