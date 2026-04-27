from create_records_3v import create_records_3v
from vrel.core.constants import AUTO
from vrel.entity.Relation import Relation
from vrel.entity.Variable import Variable
from vrel.interface.SomeDataSource import SomeDataSource
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext


class CooperModule(SomeModule):

    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("resolve_name", query_function=self.resolve_name))
        self.add_relation(Relation("not_3v", query_function=self.not_3v))
        self.add_relation(Relation("and_3v", query_function=self.and_3v))
        self.add_relation(Relation("create_records_3v", query_function=self.create_records_3v))
        self.add_relation(
            Relation(
                "metal",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "metallic",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "element",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "compound",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "solid",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "gas",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "nonmetal",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "white",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "dark_gray",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "brittle",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "oxide",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "sulfide",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "chloride",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "fuel",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "burns",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "burns_rapidly",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "combustable",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )
        self.add_relation(
            Relation(
                "gasoline",
                query_function=self.common_query,
                write_function=self.common_write,
                formal_parameters=["id", "truth"],
            )
        )

    def resolve_name(self, arguments: list, context: ExecutionContext) -> list[list]:
        id = arguments[0]
        name = arguments[1].lower()

        out_values = self.ds.select("entity", ["id", "name"], [id, name])
        if len(out_values) > 0:
            return out_values
        else:
            # if id is given, a new name is linked to that id
            if isinstance(id, Variable):
                # otherwise a new id is created for the name
                id = AUTO
            self.ds.insert(
                "entity",
                [
                    "id",
                    "name",
                ],
                [id, name],
            )
            out_values = self.ds.select("entity", ["id", "name"], [Variable("Id"), name])
            id = out_values[0][0]

            return [[id, None]]

    # ('not_3v', in, out)
    def not_3v(self, arguments: list, context: ExecutionContext) -> list[list]:

        value = arguments[0]

        if value == "true":
            return [[None, "false"]]
        elif value == "false":
            return [[None, "true"]]
        else:
            return [[None, "unknown"]]

    # ('and_3v', atoms1, atoms2, truth1, truth2, out)
    def and_3v(self, arguments: list, context: ExecutionContext) -> list[list]:

        atoms1, atoms2, var1, var2, _ = arguments

        results1 = context.solver.solve(atoms1)
        results2 = context.solver.solve(atoms2)

        truth1 = results1[0][var1.name] if len(results1) > 0 else "unknown"
        truth2 = results2[0][var2.name] if len(results2) > 0 else "unknown"

        if truth1 == "true" and truth2 == "false":
            return [[None, None, None, None, "false"]]
        elif truth1 == "true" and truth2 == "unknown":
            return [[None, None, None, None, "unknown"]]
        elif truth1 == "true" and truth2 == "true":
            return [[None, None, None, None, "true"]]

        elif truth1 == "false" and truth2 == "false":
            return [[None, None, None, None, "false"]]
        elif truth1 == "false" and truth2 == "unknown":
            return [[None, None, None, None, "unknown"]]
        elif truth1 == "false" and truth2 == "true":
            return [[None, None, None, None, "false"]]

        elif truth1 == "unknown" and truth2 == "false":
            return [[None, None, None, None, "unknown"]]
        elif truth1 == "unknown" and truth2 == "unknown":
            return [[None, None, None, None, "unknown"]]
        elif truth1 == "unknown" and truth2 == "true":
            return [[None, None, None, None, "unknown"]]

        raise Exception(f"'and_3v' doesn't accept arguments: {arguments}")

    def create_records_3v(self, arguments: list, context: ExecutionContext) -> list[list]:
        atoms = arguments[0]
        result = create_records_3v(atoms)
        return [[None, result]]

    def common_query(self, arguments: list, context: ExecutionContext) -> list[list]:
        results = self.ds.select(context.relation.predicate, context.relation.formal_parameters, arguments)
        if len(results) > 0:
            return results
        else:
            return []

    def common_write(self, arguments: list, context: ExecutionContext) -> list[list]:
        self.ds.insert(context.relation.predicate, context.relation.formal_parameters, arguments)
