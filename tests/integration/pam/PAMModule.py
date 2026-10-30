from vrel.core.constants import FUNCTION_INDIRECT_OBJECT, FUNCTION_OBJECT, FUNCTION_SUBJECT
from vrel.entity.Id import Id
from vrel.entity.Relation import Parameter, Relation
from vrel.entity.Variable import Variable
from vrel.interface.SomeDataSource import SomeDataSource
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.module.PlainReadWriteModule import PlainReadWriteModule


class PAMModule(PlainReadWriteModule):

    def __init__(self) -> None:
        super().__init__()

        self.add_relation(
            Relation(
                "resolve_name",
                parameters=[Parameter("id", int), Parameter("name", str)],
                query_function=self.resolve_name,
            )
        )

        self.add_relation(
            Relation(
                "name",
                query_function=self.common_query,
                write_function=self.common_write,
                parameters=[Parameter("id", str), Parameter("name", str)],
            )
        )

        self.add_relation(
            Relation(
                "get_into",
                parameters=[
                    Parameter("id", "event"),
                    Parameter("subject", "person", function=FUNCTION_SUBJECT),
                    Parameter("object", "thing", function=FUNCTION_OBJECT),
                ],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "pick_up",
                parameters=[
                    Parameter("id", "event"),
                    Parameter("subject", "person", function=FUNCTION_SUBJECT),
                    Parameter("object", "thing", function=FUNCTION_OBJECT),
                ],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "pull_over",
                parameters=[Parameter("id", "event"), Parameter("subject", "person", function=FUNCTION_SUBJECT)],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "to",
                parameters=[Parameter("id", "event"), Parameter("object", "thing", function=FUNCTION_OBJECT)],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "ask",
                parameters=[
                    Parameter("id", "event"),
                    Parameter("subject", "person", function=FUNCTION_SUBJECT),
                    Parameter("object", "person", function=FUNCTION_OBJECT),
                    Parameter("question", "event", function=FUNCTION_INDIRECT_OBJECT),
                ],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "tell",
                parameters=[
                    Parameter("id", "event"),
                    Parameter("subject", "person", function=FUNCTION_SUBJECT),
                    Parameter("object", "person", function=FUNCTION_OBJECT),
                    Parameter("fact", "event", function=FUNCTION_INDIRECT_OBJECT),
                ],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "stand",
                parameters=[
                    Parameter("id", "event"),
                    Parameter("subject", "person", function=FUNCTION_SUBJECT),
                ],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "where",
                parameters=[
                    Parameter("id", "event"),
                    Parameter("fact", "event"),
                ],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "by",
                parameters=[
                    Parameter("id", "event"),
                    Parameter("object", "object", function=FUNCTION_OBJECT),
                ],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "of",
                parameters=[
                    Parameter("id", "thing"),
                    Parameter("object", "thing"),
                ],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "be",
                parameters=[
                    Parameter("id", "event"),
                    Parameter("subject", "person", function=FUNCTION_SUBJECT),
                ],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "hungry",
                parameters=[Parameter("id", "event"), Parameter("subject", "person")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "lost",
                parameters=[Parameter("id", "event"), Parameter("subject", "person", function=FUNCTION_SUBJECT)],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "plan",
                parameters=[Parameter("content", "event")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "goal",
                parameters=[Parameter("content", "event")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "side",
                parameters=[Parameter("id", "thing")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "road",
                parameters=[Parameter("id", "thing")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "car",
                parameters=[Parameter("id", "car")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "farmer",
                parameters=[Parameter("id", "farmer")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "she",
                parameters=[Parameter("id", "person")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "her",
                parameters=[Parameter("id", "person")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "him",
                parameters=[Parameter("id", "person")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "he",
                parameters=[Parameter("id", "person")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "michelin_guide",
                parameters=[Parameter("id", "book")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )

    def common_write(self, arguments: list, context: ExecutionContext) -> list[list]:
        print("WRITE", arguments)
        self.insert(context.relation, context.relation.get_parameter_names(), arguments)

    def common_query(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.select(context.relation, context.relation.get_parameter_names(), arguments)

    def resolve_name(self, arguments: list, context: ExecutionContext) -> list[list]:
        id = arguments[0]
        name = arguments[1]

        name_relation = self.get_relation("name")

        if isinstance(name, str):
            arg_id = Id(name, "person")
            self.insert(name_relation, ["id", "name"], [arg_id, name])
            return [[arg_id, name]]

        out_values = self.select(name_relation, ["id", "name"], [id, name])
        return out_values
