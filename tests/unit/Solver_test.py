import sqlite3
import unittest

from vrel.core.Model import Model
from vrel.core.constants import E1, E2
from vrel.data_source.Sqlite3DataSource import Sqlite3DataSource
from vrel.entity.Atom import Atom
from vrel.entity.Id import Id
from vrel.entity.Variable import Variable
from vrel.entity.Relation import Parameter, Relation
from vrel.interface.SomeDataSource import SomeDataSource
from vrel.core.Solver import Solver
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext


class SimpleModule(SomeModule):
    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.data_source = data_source
        self.add_relation(Relation("river", parameters=[Parameter("id", "entity")], query_function=self.simple_entity))
        self.add_relation(
            Relation("country", parameters=[Parameter("id", "entity")], query_function=self.simple_entity)
        )
        self.add_relation(
            Relation(
                "contains",
                parameters=[Parameter("country", "entity"), Parameter("river", "entity")],
                query_function=self.contains,
            )
        )
        self.add_relation(
            Relation(
                "number_of",
                parameters=[Parameter("id1", "entity"), Parameter("number", int)],
                query_function=self.number_of,
            )
        )

    def simple_entity(self, arguments: list, context: ExecutionContext) -> list[list]:
        out_values = self.select(context.relation, ["id"], arguments)
        return out_values

    def contains(self, arguments: list, context: ExecutionContext) -> list[list]:
        out_values = self.select(context.relation, ["country", "river"], arguments)
        return out_values

    def number_of(self, arguments: list, context: ExecutionContext) -> list[list]:
        if arguments[1] == 2:
            out_values = [[None, 2]]
        else:
            out_values = []
        return out_values


class TestSolver(unittest.TestCase):

    def test_solver(self):

        connection = sqlite3.connect(":memory:")
        cursor = connection.cursor()
        data_source = Sqlite3DataSource(connection)

        # note: same entity may have multiple names
        cursor.execute("CREATE TABLE river (id TEXT)")
        cursor.execute("CREATE TABLE country (id TEXT)")
        cursor.execute("CREATE TABLE contains (country TEXT, river TEXT)")

        data_source.insert("river", ["id"], ["amazon"])
        data_source.insert("river", ["id"], ["brahmaputra"])

        data_source.insert("country", ["id"], ["brasil"])
        data_source.insert("country", ["id"], ["india"])

        data_source.insert("contains", ["country", "river"], ["brasil", "amazon"])
        data_source.insert("contains", ["country", "river"], ["india", "brahmaputra"])

        model = Model([SimpleModule(data_source)])
        solver = Solver(model)

        tests = [
            [[Atom("river", E1)], [{"E1": Id("amazon", "entity")}, {"E1": Id("brahmaputra", "entity")}]],
            [[Atom("river", E1), Atom("contains", "india", E1)], [{"E1": Id("brahmaputra", "entity")}]],
            [
                [Atom("contains", E1, E2), Atom("country", E1)],
                [
                    {"E1": Id("brasil", "entity"), "E2": Id("amazon", "entity")},
                    {"E1": Id("india", "entity"), "E2": Id("brahmaputra", "entity")},
                ],
            ],
            [[Atom("contains", E1, E1)], []],
            # number_of returns 2; this doesn't match 3
            [[Atom("number_of", "river", 3)], []],
            # number_of returns 2; and it matches
            [[Atom("number_of", "river", 2)], [{}]],
            # unification
            [
                [Atom("$unification", E2, E1), Atom("river", E1), Atom("contains", "india", E2)],
                [{"E1": Id("brahmaputra", "entity"), "E2": Variable("E1")}],
            ],
        ]

        for test in tests:
            question, answer = test
            result = solver.solve(question)
            self.assertEqual(answer, result)
