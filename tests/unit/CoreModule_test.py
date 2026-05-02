import unittest

from resolve_name.SimpleModule import SimpleModule
from resolve_name.SimpleDB import SimpleDB
from vrel.core.Model import Model
from vrel.core.Solver import Solver
from vrel.core.constants import E1, E2, E3, E4, E5
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.module.CoreModule import CoreModule
from vrel.module.transform.resolve_names import resolve_names


class TestCoreModule(unittest.TestCase):

    core_module: CoreModule

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.core_module = CoreModule()

    def test_equals(self):

        bindings = self.core_module.equals([3, 5], None)
        self.assertEqual(bindings, [])

        bindings = self.core_module.equals([3, 3], None)
        self.assertEqual(bindings, [[3, 3]])

        bindings = self.core_module.equals([3, Variable("E1")], None)
        self.assertEqual(bindings, [[3, 3]])

        bindings = self.core_module.equals([Variable("E1"), 3], None)
        self.assertEqual(bindings, [[3, 3]])

    def test_let(self):

        model = Model([])
        solver = Solver(model)

        bindings = solver.solve([Atom("let", E1, 5)])
        self.assertEqual(bindings, [{"E1": 5}])

    def test_scope(self):

        model = Model([])
        solver = Solver(model)

        bindings = solver.solve([Atom("scope", [Atom("let", E1, 3)])])
        self.assertEqual(bindings, [{}])

        bindings = solver.solve([Atom("scope", [Atom("equals", 2, 3)])])
        self.assertEqual(bindings, [])

    def test_exec(self):

        model = Model([])
        solver = Solver(model)

        bindings = solver.solve([Atom("exec", [Atom("let", E1, 3)], [Atom("let", E2, E1)])])
        self.assertEqual(bindings, [{"E1": 3, "E2": 3}])

        bindings = solver.solve([Atom("exec", [Atom("equals", 2, 3)])])
        self.assertEqual(bindings, [])

    def test_unification(self):

        model = Model([])
        solver = Solver(model)

        source = [
            Atom("alive", "john"),
            Atom("lost", "john"),
            Atom("likes", "john", "jane"),
            Atom("goal", "john", Atom("win", "jane")),
        ]

        bindings = solver.solve([Atom("$unification", source, [Atom("lost", E1)])])
        self.assertEqual(bindings, [{"E1": "john"}])

        bindings = solver.solve([Atom("$unification", source, [Atom("location", E1)])])
        self.assertEqual(bindings, [])

        bindings = solver.solve([Atom("$unification", source, [Atom("likes", E1, "jane")])])
        self.assertEqual(bindings, [{"E1": "john"}])

        bindings = solver.solve([Atom("$unification", source, [Atom("likes", E1, E1)])])
        self.assertEqual(bindings, [])

        bindings = solver.solve([Atom("$unification", source, [Atom("lost", E1), Atom("likes", E1, E2)])])
        self.assertEqual(bindings, [{"E1": "john", "E2": "jane"}])

        bindings = solver.solve([Atom("$unification", [Atom("lost", E1), Atom("likes", E1, E2)], source)])
        self.assertEqual(bindings, [{"E1": "john", "E2": "jane"}])

        bindings = solver.solve([Atom("$unification", source, [Atom("lost", E1), Atom("hates", E1, E2)])])
        self.assertEqual(bindings, [])

        bindings = solver.solve([Atom("$unification", [Atom("lost", E1), Atom("hates", E1, E2)], source)])
        self.assertEqual(bindings, [])

        bindings = solver.solve([Atom("$unification", source, [Atom("goal", E1, Atom("win", E2))])])
        self.assertEqual(bindings, [{"E1": "john", "E2": "jane"}])

        bindings = solver.solve([Atom("$unification", source, [Atom("goal", E1, Atom("win", E1))])])
        self.assertEqual(bindings, [])

        bindings = solver.solve([Atom("let", E2, "mary"), Atom("$unification", source, [Atom("lost", E1)])])
        self.assertEqual(bindings, [{"E1": "john", "E2": "mary"}])

        bindings = solver.solve([Atom("let", E1, "mary"), Atom("$unification", source, [Atom("lost", E1)])])
        self.assertEqual(bindings, [])

        # # target, source
        bindings = solver.solve([Atom("$unification", [Atom("likes", E1, "jane")], source)])
        self.assertEqual(bindings, [{"E1": "john"}])

        bindings = solver.solve([Atom("$unification", [Atom("lost", E1)], source)])
        self.assertEqual(bindings, [{"E1": "john"}])

        # unbound variables
        bindings = solver.solve(
            [
                Atom("$unification", E1, E2),
                Atom("$unification", source, [Atom("goal", E1, Atom("win", E2))]),
            ]
        )
        self.assertEqual(bindings, [])

        bindings = solver.solve(
            [
                Atom("$unification", source, [Atom("goal", E1, Atom("win", E2))]),
                Atom("$unification", E1, E2),
            ]
        )
        self.assertEqual(bindings, [])

        bindings = solver.solve(
            [
                Atom("$unification", E1, E3),
                Atom("$unification", E2, E3),
                Atom("$unification", source, [Atom("goal", E1, Atom("win", E2))]),
            ]
        )
        self.assertEqual(bindings, [])

        bindings = solver.solve(
            [
                Atom("$unification", source, [Atom("goal", E1, Atom("win", E2))]),
                Atom("$unification", E1, E3),
                Atom("$unification", E2, E3),
            ]
        )
        self.assertEqual(bindings, [])

        bindings = solver.solve(
            [
                Atom("$unification", E1, E2),
                Atom("$unification", E3, E4),
                Atom("$unification", Atom("red", E5), E4),
                Atom("$unification", E1, E4),
            ]
        )
        self.assertEqual(
            bindings,
            [
                {
                    "E1": E2,
                    "E3": E4,
                    "E4": Atom("red", E5),
                    "E2": Atom("red", E5),
                }
            ],
        )

        bindings = solver.solve(
            [
                Atom(
                    "$unification",
                    [Atom("likes", E1, "jane")],
                    [Atom("likes", "john", E1)],
                ),
            ]
        )
        self.assertEqual(bindings, [])

        bindings = solver.solve(
            [
                Atom(
                    "$unification",
                    [Atom("full_isa", E1, E1)],
                    [Atom("full_isa", E2, "finger")],
                )
            ]
        )
        self.assertEqual(bindings, [{"E1": E2, "E2": "finger"}])

    def test_resolve_name(self):
        data_source = SimpleDB()
        facts = SimpleModule(data_source)

        model = Model([facts])
        solver = Solver(model)

        # auto-generate id's for new names
        atoms = [Atom("name", E1, "John"), Atom("name", E2, "Mary"), Atom("likes", E1, E2)]
        result = resolve_names(atoms, solver)
        self.assertEqual(result, [Atom("likes", 1, 2)])

        # retrieve these id's for the same names
        atoms = [Atom("name", E1, "John"), Atom("name", E2, "Mary"), Atom("likes", E1, E2)]
        result = resolve_names(atoms, solver)
        self.assertEqual(result, [Atom("likes", 1, 2)])

        # in modifier
        atoms = [Atom("likes", E1, E2).any([Atom("name", E1, "John"), Atom("name", E2, "Mary")])]
        result = resolve_names(atoms, solver)
        self.assertEqual(result, [Atom("likes", 1, 2)])

        # in argument
        atoms = [
            Atom("likes", E1, [Atom("surprise", E1, E2)]).any([Atom("name", E1, "John"), Atom("name", E2, "Mary")])
        ]
        result = resolve_names(atoms, solver)
        self.assertEqual(result, [Atom("likes", 1, [Atom("surprise", 1, 2)])])

        atoms = [Atom("likes", E1, [Atom("surprise", E1, Atom("name", E2, "Mary"))]).any([Atom("name", E1, "John")])]
        result = resolve_names(atoms, solver)
        self.assertEqual(result, [Atom("likes", 1, [Atom("surprise", 1, 2)])])
