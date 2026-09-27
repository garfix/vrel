import unittest

from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.entity.InductionRule import InductionRule
from vrel.dsl.SimpleInferenceRuleParser import SimpleInferenceRuleParser


class TestInductionModule(unittest.TestCase):

    def test_simple_inference_rule_parser(self):
        parser = SimpleInferenceRuleParser()

        tests = [
            [
                "orang_utan(E1) => ape(E1).",
                [InductionRule([Atom("orang_utan", Variable("E1"))], [Atom("ape", Variable("E1"))], None)],
            ],
            [
                "female(E1), cow(E1), young(E1) => heifer(E1), bovine(E1).",
                [
                    InductionRule(
                        [
                            Atom("female", Variable("E1")),
                            Atom("cow", Variable("E1")),
                            Atom("young", Variable("E1")),
                        ],
                        [
                            Atom("heifer", Variable("E1")),
                            Atom("bovine", Variable("E1")),
                        ],
                        None,
                    )
                ],
            ],
            [
                "near(E1, E2) => ask(E1, E2, F1) => know(E1, F1).",
                [
                    InductionRule(
                        [
                            Atom("near", Variable("E1"), Variable("E2")),
                        ],
                        [
                            Atom("know", Variable("E1"), Variable("F1")),
                        ],
                        [
                            Atom("ask", Variable("E1"), Variable("E2"), Variable("F1")),
                        ],
                    )
                ],
            ],
        ]

        for test in tests:
            question, answer = test
            induction_rules, _ = parser.parse_induction_rules(question)
            self.assertEqual(answer, induction_rules)
