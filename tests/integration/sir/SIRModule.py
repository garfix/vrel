from vrel.entity.Atom import Atom
from vrel.entity.BindingResult import BindingResult
from vrel.entity.Id import Id
from vrel.entity.Relation import Parameter, Relation
from vrel.entity.Variable import Variable
from vrel.interface.SomeDataSource import SomeDataSource
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext


class SIRModule(SomeModule):

    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.data_source = data_source
        self.add_relation(
            Relation(
                "resolve_name",
                parameters=[Parameter("id", str), Parameter("name", str)],
                query_function=self.resolve_name,
            )
        )
        self.add_relation(Relation("finger", parameters=[Parameter("id", "finger")], query_function=self.finger))
        self.add_relation(
            Relation(
                "have", parameters=[Parameter("whole", "thing"), Parameter("part", "thing")], query_function=self.have
            )
        )
        self.add_relation(
            Relation(
                "part_of",
                query_function=self.common_query,
                write_function=self.common_write,
                parameters=[Parameter("part", "thing"), Parameter("whole", "thing")],
            )
        ),
        self.add_relation(
            Relation(
                "part_of_n",
                query_function=self.part_of_n,
                write_function=self.common_write,
                parameters=[Parameter("part", "thing"), Parameter("whole", "thing"), Parameter("number", int)],
            )
        ),
        self.add_relation(
            Relation(
                "isa",
                query_function=self.common_query,
                write_function=self.common_write,
                parameters=[Parameter("entity", "thing"), Parameter("type", "thing")],
            )
        ),
        self.add_relation(
            Relation(
                "identical",
                query_function=self.common_query,
                write_function=self.common_write,
                parameters=[Parameter("entity1", "thing"), Parameter("entity2", "thing")],
            )
        ),
        self.add_relation(
            Relation(
                "own",
                query_function=self.common_query,
                write_function=self.common_write,
                parameters=[Parameter("person", "thing"), Parameter("thing", "thing")],
            )
        ),
        self.add_relation(
            Relation(
                "just_left_of",
                query_function=self.common_query,
                write_function=self.common_write,
                parameters=[Parameter("thing1", "thing"), Parameter("thing2", "thing")],
            )
        ),
        self.add_relation(
            Relation(
                "left_of",
                query_function=self.common_query,
                write_function=self.common_write,
                parameters=[Parameter("thing1", "thing"), Parameter("thing2", "thing")],
            )
        ),

        # used in write_grammar.py
        self.add_relation(
            Relation(
                "position_description",
                query_function=self.position_description,
                parameters=[Parameter("description", str)],
            )
        ),

    def common_query(self, arguments: list, context: ExecutionContext) -> list[list]:
        results = self.select(context.relation, context.relation.get_parameter_names(), arguments)
        return results

    def common_write(self, arguments: list, context: ExecutionContext) -> list[list]:
        self.insert(context.relation, context.relation.get_parameter_names(), arguments)

    def part_of_n(self, arguments: list, context: ExecutionContext) -> list[list]:
        part_variable = arguments[0]
        whole_variable = arguments[1]

        whole_type = whole_variable
        part_type = self.get_type(context, part_variable, part_variable)

        results = self.select(context.relation, context.relation.get_parameter_names(), arguments)

        if len(results) == 0:
            if part_type is not None and whole_type is not None:

                # produce output
                context.solver.solve(
                    [
                        Atom(
                            "store",
                            [
                                Atom("output_type", "how_many"),
                                Atom("output_how_many", part_type, whole_type.id),
                            ],
                        )
                    ]
                )

        return results

    # resolve(id, name)
    def resolve_name(self, arguments: list, context: ExecutionContext) -> list[list]:
        name = arguments[1]

        return [[Id(name, "person"), name]]

    # finger(id)
    def finger(self, arguments: list, context: ExecutionContext) -> list[list]:

        # no individual fingers are available, but we must return at least one
        return [[Id("a-finger", "thing")]]

    # have(whole, part)
    # the verb have is always very abstract, but in this case it also handles with information on the class-level
    def have(self, arguments: list, context: ExecutionContext) -> list[list]:

        # solving based on class information

        whole_variable = arguments[0]
        part_variable = arguments[1]

        whole_type = whole_variable
        part_type = self.get_type(context, part_variable, part_variable)
        results = context.solver.solve([Atom("part_of_number", part_type, whole_type, Variable("N"))])

        if len(results) == 0:
            # produce output
            context.solver.solve(
                [
                    Atom(
                        "store",
                        [
                            Atom("output_type", "dont_know_part_of"),
                            Atom("output_dont_know_part_of", part_type, whole_type.id),
                        ],
                    )
                ]
            )
            return []

        number = results[0]["N"]

        return BindingResult([{"A": n} for n in range(number)])

    def get_type(self, context: ExecutionContext, id: str, value):
        if isinstance(id, Id) and id.id == "a-finger":
            return "finger"

        return value

    # used in write_grammar.py to create complex output
    def position_description(self, arguments: list, context: ExecutionContext) -> list[list]:
        # working out the algorithm described in the article is left to the interested reader
        return [["<the ordered list>"]]
