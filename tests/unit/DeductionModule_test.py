import pathlib
import unittest

from vrel.core.Model import Model
from vrel.core.constants import E1, E2
from vrel.core.Solver import Solver
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.module.DeductionModule import DeductionModule
from vrel.dsl.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from vrel.entity.InferenceRule import InferenceRule


class TestDeductionModule(unittest.TestCase):

    def test_deduction_module(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/deduction/"

        inferences = DeductionModule()
        inferences.import_rules(path + "rules.pl")

        model = Model([inferences])
        solver = Solver(model)

        tests = [
            # [[Atom("river", "brahma_putra")], [{}]],
            # [[Atom("river", "amazon")], [{}]],
            # [
            #     [Atom("grand_parent", E1, E2)],
            #     [
            #         {"E1": "robert", "E2": "william"},
            #         {"E1": "martha", "E2": "beatrice"},
            #         {"E1": "martha", "E2": "antonio"},
            #     ],
            # ],
            [[Atom("grand_parent", "robert", "william")], [{}]],
            # [
            #     [Atom("grand_parent", "martha", E2)],
            #     [{"E2": "beatrice"}, {"E2": "antonio"}],
            # ],
            # [[Atom("grand_parent", E1, "antonio")], [{"E1": "martha"}]],
            # [[Atom("grand_parent", "martha", "antonio")], [{}]],
            # [[Atom("grand_parent", "martha", "edward")], []],
            # # bindings are passed
            # [
            #     [Atom("knows", [Atom("parent", "martha", E2)], "true")],
            #     [{"E2": "william"}],
            # ],
            # [[Atom("knows", [Atom("parent", "magdalena", E2)], "true")], []],
            # [[Atom("ancestor", "robert", "antonio")], [{}]],
            # [[Atom("related", "robert", "antonio")], [{}]],
            # [[Atom("related", "robert", "robert")], [{}]],
            # [[Atom("related", "robert", "xantippe")], []],
            # [[Atom("related", "jennifer", "jennifer")], [{}]],
            # [[Atom("related", "robert", "robert")], [{}]],
            # # test disjunction
            # [[Atom("family", E1, "martha")], [{"E1": "robert"}]],
            # [[Atom("family", E1, "william")], [{"E1": "robert"}]],
            # [[Atom("sibling", "spike", E1)], [{"E1": "suzy"}]],
            # [[Atom("country", E1)], [{"E1": "netherlands"}]],
        ]

        for test in tests:
            question, answer = test
            result = solver.solve(question)
            self.assertEqual(answer, result)
