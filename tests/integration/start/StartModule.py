from datetime import date

from vrel.entity.Relation import Parameter, Relation
from vrel.interface.SomeDataSource import SomeDataSource
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext


class StartModule(SomeModule):

    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()

        self.data_source = data_source

        self.add_relation(
            Relation(
                "employee",
                query_function=self.simple_entity,
                parameters=[
                    Parameter("id", "person"),
                    Parameter("name", str),
                    Parameter("birth_date", date),
                ],
            )
        )

        self.add_relation(
            Relation(
                "age",
                query_function=self.age,
                parameters=[
                    Parameter("id", "person"),
                    Parameter("age", float),
                ],
            )
        )

    def simple_entity(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.select(context.relation, ["id"], arguments)

    def age(self, arguments: list, context: ExecutionContext) -> list[list]:
        results = self.select(self.get_relation("employee"), ["id", "birth_date"], arguments)

        ages = [[result[0], calculate_age(result[1])] for result in results]
        return ages


def calculate_age(birth_date: str) -> int:
    birth = date.fromisoformat(birth_date)  # parses "yyyy-mm-dd"
    today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
