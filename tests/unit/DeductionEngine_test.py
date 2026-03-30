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

    def test_simple_inference_rule_parser(self):
        parser = SimpleInferenceRuleParser()

        tests = [
            ["river('amazon').", [InferenceRule(("river", "amazon"), [])]],
            # with comment
            ["river('amazon')\n\t#remark\n.", [InferenceRule(("river", "amazon"), [])]],
            ["mountain('Dante\\'s peak').", [InferenceRule(("mountain", "Dante's peak"), [])]],
            ['person("Robert \\"Bobby\\" Brown").', [InferenceRule(("person", 'Robert "Bobby" Brown'), [])]],
            ["river().", [InferenceRule(("river",), [])]],
            ["population('france', 43).", [InferenceRule(("population", "france", 43), [])]],
            ["constant('pi', 3.14159265359).", [InferenceRule(("constant", "pi", 3.14159265359), [])]],
            [
                "father(E1, E2) :- parent(E1, E2), father(E1).",
                [
                    InferenceRule(
                        ("father", Variable("E1"), Variable("E2")),
                        [("parent", Variable("E1"), Variable("E2")), ("father", Variable("E1"))],
                    )
                ],
            ],
            [
                "childless(E1) :- not(parent(E1, E2)).",
                [InferenceRule(("childless", Variable("E1")), [("not", [("parent", Variable("E1"), Variable("E2"))])])],
            ],
            # grouped atoms with parenthesis
            [
                "switch(E1) :- or((a(1), b(2)), (c(3), d(4))).",
                [
                    InferenceRule(
                        ("switch", Variable("E1")),
                        [
                            (
                                "or",
                                [("a", 1), ("b", 2)],
                                [("c", 3), ("d", 4)],
                            )
                        ],
                    )
                ],
            ],
            # unification
            ["pred(X) :- X = 2.", [InferenceRule(("pred", Variable("X")), [("$unification", Variable("X"), 2)])]],
            [
                "pred(X) :- X = pred2(A).",
                [InferenceRule(("pred", Variable("X")), [("$unification", Variable("X"), [("pred2", Variable("A"))])])],
            ],
            [
                "pred(X) :- pred2(A) = X.",
                [InferenceRule(("pred", Variable("X")), [("$unification", [("pred2", Variable("A"))], Variable("X"))])],
            ],
        ]

        for test in tests:
            question, answer = test
            rules, _ = parser.parse_rules(question)
            self.assertEqual(answer, rules)

    def test_deduction_module(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/inference/"

        inferences = DeductionModule()
        inferences.import_rules(path + "rules.pl")

        model = Model([inferences])
        solver = Solver(model)

        tests = [
            [[Atom("river", "brahma_putra")], [{}]],
            [[Atom("river", "amazon")], [{}]],
            [
                [Atom("grand_parent", E1, E2)],
                [
                    {"E1": "robert", "E2": "william"},
                    {"E1": "martha", "E2": "beatrice"},
                    {"E1": "martha", "E2": "antonio"},
                ],
            ],
            [[Atom("grand_parent", "robert", "william")], [{}]],
            [[Atom("grand_parent", "martha", E2)], [{"E2": "beatrice"}, {"E2": "antonio"}]],
            [[Atom("grand_parent", E1, "antonio")], [{"E1": "martha"}]],
            [[Atom("grand_parent", "martha", "antonio")], [{}]],
            [[Atom("grand_parent", "martha", "edward")], []],
            # bindings are passed
            [[Atom("knows", [("parent", "martha", E2)], "true")], [{"E2": "william"}]],
            [[Atom("knows", [("parent", "magdalena", E2)], "true")], []],
            [[Atom("ancestor", "robert", "antonio")], [{}]],
            [[Atom("related", "robert", "antonio")], [{}]],
            [[Atom("related", "robert", "robert")], [{}]],
            [[Atom("related", "robert", "xantippe")], []],
            [[Atom("related", "jennifer", "jennifer")], [{}]],
            [[Atom("related", "robert", "robert")], [{}]],
            # test disjunction
            [[Atom("family", E1, "martha")], [{"E1": "robert"}]],
            [[Atom("family", E1, "william")], [{"E1": "robert"}]],
            [[Atom("sibling", "spike", E1)], [{"E1": "suzy"}]],
            [[Atom("country", E1)], [{"E1": "netherlands"}]],
        ]

        for test in tests:
            question, answer = test
            result = solver.solve(question)
            self.assertEqual(answer, result)
