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

        # self.add_relation(Relation("hungry", query_function=self.simple_entity))
        # self.add_relation(Relation("michelin_guide", query_function=self.simple_entity))
        # self.add_relation(Relation("pick_up", query_function=self.common_query, formal_parameters=['id1', 'id2', 'id3'], write_function=self.common_write))
        self.add_relation(
            Relation(
                "get_into",
                parameters=[Parameter("id", "event"), Parameter("subject", "person"), Parameter("object", "thing")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        self.add_relation(
            Relation(
                "pick_up",
                parameters=[Parameter("id", "event"), Parameter("subject", "person"), Parameter("object", "thing")],
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
                "car",
                parameters=[Parameter("id", "car")],
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
                "michelin_guide",
                parameters=[Parameter("id", "book")],
                query_function=self.common_query,
                write_function=self.common_write,
            )
        )
        # self.add_relation(Relation("car", query_function=self.simple_entity))
        # self.add_relation(Relation("name", query_function=self.simple_entity))
        # self.add_relation(Relation("female", query_function=self.simple_entity))
        # self.add_relation(Relation("person", query_function=self.simple_entity))
        # self.add_relation(Relation("her", query_function=self.simple_entity))

        # self.add_relation(Relation("go_through_red_light", query_function=self.simple_entity))
        # self.add_relation(Relation("pull_over", query_function=self.simple_entity))
        # self.add_relation(Relation("summons", query_function=self.simple_entity))
        # self.add_relation(Relation("speeding", query_function=self.simple_entity))
        # self.add_relation(Relation("for", query_function=self.simple_entity))
        # self.add_relation(Relation("cop", query_function=self.simple_entity))
        # self.add_relation(Relation("get", query_function=self.simple_entity))
        # self.add_relation(Relation("previous_week", query_function=self.simple_entity))
        # self.add_relation(Relation("tell", query_function=self.simple_entity))
        # self.add_relation(Relation("if", query_function=self.simple_entity))
        # self.add_relation(Relation("he", query_function=self.simple_entity))
        # self.add_relation(Relation("another", query_function=self.simple_entity))
        # self.add_relation(Relation("violation", query_function=self.simple_entity))
        # self.add_relation(Relation("license", query_function=self.simple_entity))
        # self.add_relation(Relation("his", query_function=self.simple_entity))
        # self.add_relation(Relation("take_away", query_function=self.simple_entity))
        # self.add_relation(Relation("remember", query_function=self.simple_entity))
        # self.add_relation(Relation("game", query_function=self.simple_entity))
        # self.add_relation(Relation("poss", query_function=self.simple_entity))
        # self.add_relation(Relation("have_on_oneself", query_function=self.simple_entity))
        # self.add_relation(Relation("ticket", query_function=self.simple_entity))
        # self.add_relation(Relation("number_of", query_function=self.simple_entity))
        # self.add_relation(Relation("them", query_function=self.simple_entity))
        # self.add_relation(Relation("give", query_function=self.simple_entity))
        # self.add_relation(Relation("whole", query_function=self.simple_entity))
        # self.add_relation(Relation("incident", query_function=self.simple_entity))
        # self.add_relation(Relation("forget", query_function=self.simple_entity))
        # self.add_relation(Relation("happen", query_function=self.simple_entity))
        # self.add_relation(Relation("terrific", query_function=self.simple_entity))
        # self.add_relation(Relation("football_fan", query_function=self.simple_entity))
        # self.add_relation(Relation("take", query_function=self.simple_entity))
        # self.add_relation(Relation("drive_away", query_function=self.simple_entity))
        # self.add_relation(Relation("name", query_function=self.simple_entity))
        # self.add_relation(Relation("lost", query_function=self.simple_entity))
        # self.add_relation(Relation("farmer", query_function=self.simple_entity))
        # self.add_relation(Relation("stand", query_function=self.simple_entity))
        # self.add_relation(Relation("side", query_function=self.simple_entity))
        # self.add_relation(Relation("road", query_function=self.simple_entity))
        # self.add_relation(Relation("of", query_function=self.simple_entity))
        # self.add_relation(Relation("by", query_function=self.simple_entity))
        # self.add_relation(Relation("to", query_function=self.simple_entity))
        # self.add_relation(Relation("ask", query_function=self.simple_entity))
        # self.add_relation(Relation("be", query_function=self.simple_entity))
        # self.add_relation(Relation("male", query_function=self.simple_entity))
        # self.add_relation(Relation("person", query_function=self.simple_entity))

    def common_write(self, arguments: list, context: ExecutionContext) -> list[list]:
        self.insert(context.relation, context.relation.get_parameter_names(), arguments)

    def common_query(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.select(context.relation, context.relation.get_parameter_names(), arguments)

    def resolve_name(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[1]

        return [[Id(name, "person"), name]]
