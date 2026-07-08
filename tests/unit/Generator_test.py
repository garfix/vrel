import pathlib
import unittest

from vrel.core.BasicGenerator import BasicGenerator
from vrel.core.Model import Model
from vrel.core.Solver import Solver
from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.module.DeductionModule import DeductionModule

Id = Variable("Id")
Pred = Variable("Pred")
Subject = Variable("Subject")
Object = Variable("Object")


class TestGenerator(unittest.TestCase):

    def test_generator(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/generator/"

        inferences = DeductionModule()
        inferences.import_rules(path + "inferences.pl")

        model = Model([inferences])

        raw_grammar = [
            {"syn": "s() -> 'OK'", "if": [Atom("last_output", "ok")]},
            {
                "syn": "s() -> 'The above sentence is impossible'",
                "if": [Atom("last_output", "impossible")],
            },
            {
                "syn": "s() -> np(E2) vp(E1)",
                "if": [
                    Atom("last_output", "declarative", E1, Pred, E2, Object),
                ],
            },
            {
                "syn": "s() -> named_number(E1)",
                "if": [Atom("last_output", "scalar", E1)],
            },
            {"syn": "vp(E1) -> verb(E1) np(E2)", "if": [Atom("last_output", "declarative", E1, Pred, Subject, E2)]},
            {"syn": "np(E1) -> literal(E2)", "if": [Atom("resolve_name", E2, E1)]},
            {
                "syn": "verb(E1) -> 'married'",
                "if": [Atom("last_output", "declarative", E1, "marry", Subject, Object)],
            },
            {"syn": "named_number(E1) -> 'one'", "if": [Atom("equals", E1, 1)]},
            {"syn": "named_number(E1) -> 'two'", "if": [Atom("equals", E1, 2)]},
        ]

        generator = BasicGenerator(model)
        generator.add_grammar_rules(raw_grammar)

        tests = [
            {"atoms": [Atom("out", "ok")], "output": "OK"},
            {
                "atoms": [Atom("out", "impossible")],
                "output": "The above sentence is impossible",
            },
            {
                "atoms": [
                    Atom("out", "declarative", 5, "marry", "10892", "37216"),
                ],
                "output": "Jane married John",
            },
            # {
            #     "atoms": [Atom("last_output", "scalar", 2)],
            #     "output": "two",
            # },
        ]

        solver = Solver(model)

        for test in tests:
            for atom in test["atoms"]:
                solver.solve([atom])
            output = generator.generate_output()
            self.assertEqual(output, test["output"])
