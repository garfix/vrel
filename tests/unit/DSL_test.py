import pathlib
import unittest

from vrel.core.Model import Model
from vrel.core.constants import DISJUNCTION, E1, E2
from vrel.core.Solver import Solver
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable
from vrel.module.DeductionModule import DeductionModule
from vrel.dsl.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from vrel.entity.InferenceRule import InferenceRule


class TestDSL(unittest.TestCase):

    def test_dsl(self):
        parser = SimpleInferenceRuleParser()

        tests = [
            ["river('amazon').", [InferenceRule(Atom("river", "amazon"), [])]],
            # with comment
            [
                "river('amazon')\n\t#remark\n.",
                [InferenceRule(Atom("river", "amazon"), [])],
            ],
            [
                "mountain('Dante\\'s peak').",
                [InferenceRule(Atom("mountain", "Dante's peak"), [])],
            ],
            [
                'person("Robert \\"Bobby\\" Brown").',
                [InferenceRule(Atom("person", 'Robert "Bobby" Brown'), [])],
            ],
            [
                "river().",
                [
                    InferenceRule(
                        Atom(
                            "river",
                        ),
                        [],
                    )
                ],
            ],
            [
                "population('france', 43).",
                [InferenceRule(Atom("population", "france", 43), [])],
            ],
            [
                "constant('pi', 3.14159265359).",
                [InferenceRule(Atom("constant", "pi", 3.14159265359), [])],
            ],
            [
                "father(E1, E2) :- parent(E1, E2), father(E1).",
                [
                    InferenceRule(
                        Atom("father", Variable("E1"), Variable("E2")),
                        [
                            Atom("parent", Variable("E1"), Variable("E2")),
                            Atom("father", Variable("E1")),
                        ],
                    )
                ],
            ],
            [
                "childless(E1) :- not(parent(E1, E2)).",
                [
                    InferenceRule(
                        Atom("childless", Variable("E1")),
                        [Atom("not", [Atom("parent", Variable("E1"), Variable("E2"))])],
                    )
                ],
            ],
            # grouped atoms with parenthesis
            [
                "switch(E1) :- or((a(1), b(2)), (c(3), d(4))).",
                [
                    InferenceRule(
                        Atom("switch", Variable("E1")),
                        [
                            Atom(
                                "or",
                                [Atom("a", 1), Atom("b", 2)],
                                [Atom("c", 3), Atom("d", 4)],
                            )
                        ],
                    )
                ],
            ],
            [
                "switch(E1) :- (a(1), b(2) ; c(3), d(4)).",
                [
                    InferenceRule(
                        Atom("switch", Variable("E1")),
                        [
                            Atom(
                                DISJUNCTION,
                                [
                                    [Atom("a", 1), Atom("b", 2)],
                                    [Atom("c", 3), Atom("d", 4)],
                                ],
                            )
                        ],
                    )
                ],
            ],
            [
                "switch(E1) :- (a(1), b(2) ; c(3), d(4) ; c(5), d(6)).",
                [
                    InferenceRule(
                        Atom("switch", Variable("E1")),
                        [
                            Atom(
                                DISJUNCTION,
                                [
                                    [Atom("a", 1), Atom("b", 2)],
                                    [Atom("c", 3), Atom("d", 4)],
                                    [Atom("c", 5), Atom("d", 6)],
                                ],
                            )
                        ],
                    )
                ],
            ],
            # unification
            [
                "pred(X) :- X = 2.",
                [
                    InferenceRule(
                        Atom("pred", Variable("X")),
                        [Atom("$unification", Variable("X"), 2)],
                    )
                ],
            ],
            [
                "pred(X) :- X = pred2(A).",
                [
                    InferenceRule(
                        Atom("pred", Variable("X")),
                        [
                            Atom(
                                "$unification",
                                Variable("X"),
                                [Atom("pred2", Variable("A"))],
                            )
                        ],
                    )
                ],
            ],
            [
                "pred(X) :- pred2(A) = X.",
                [
                    InferenceRule(
                        Atom("pred", Variable("X")),
                        [
                            Atom(
                                "$unification",
                                [Atom("pred2", Variable("A"))],
                                Variable("X"),
                            )
                        ],
                    )
                ],
            ],
            [
                "father(parent(E1, E2), E2).",
                [
                    InferenceRule(
                        Atom("father", [Atom("parent", Variable("E1"), Variable("E2"))], Variable("E2")),
                        [],
                    )
                ],
            ],
        ]

        for test in tests:
            question, answer = test
            rules, _ = parser.parse_rules(question)
            self.assertEqual(answer, rules)
