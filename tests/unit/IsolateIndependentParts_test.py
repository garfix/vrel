import unittest

from vrel.core.constants import E1, E2, E3, E4
from vrel.entity.Atom import Atom
from vrel.module.optimizer.IsolateIndependentParts import IsolateIndependentParts


class TestIsolateIndependentParts(unittest.TestCase):

    def test_simple_inference_rule_parser(self):

        tests = [
            # simplest case: E2 depends only on E1 and no other variable depends on E2
            [[Atom("a", E1), Atom("b", E1, E2)], [], [Atom("a", E1), Atom("scope", [Atom("b", E1, E2)])]],
            # typical case: two isolated parts
            [
                [Atom("a", E1), Atom("b", E1, E2), Atom("c", E2), Atom("d", E1, E3), Atom("e", E3)],
                [],
                [
                    Atom("a", E1),
                    Atom("scope", [Atom("b", E1, E2), Atom("scope", [Atom("c", E2)])]),
                    Atom("scope", [Atom("d", E1, E3), Atom("scope", [Atom("e", E3)])]),
                ],
            ],
            # root variable: E2 depends only on E1 but E2 is used in the result
            [[Atom("a", E1), Atom("b", E1, E2)], ["E2"], [Atom("a", E1), Atom("b", E1, E2)]],
            # complex dependencies: has_population depends on city, but can't be isolated because > uses it
            [
                [
                    Atom("contains", E4, E1),
                    Atom("city", E1),
                    Atom("has_population", E1, E2),
                    Atom("=", E3, 1000000),
                    Atom(">", E2, E3),
                ],
                [],
                [
                    Atom("contains", E4, E1),
                    Atom("scope", [Atom("city", E1)]),
                    Atom(
                        "scope",
                        [
                            Atom("has_population", E1, E2),
                            Atom("scope", [Atom("=", E3, 1000000), Atom("scope", [Atom(">", E2, E3)])]),
                        ],
                    ),
                ],
            ],
            # regression test
            [
                [
                    Atom("resolve_name", "magnesium", E1),
                    Atom("resolve_name", "metal", E2),
                    Atom("isa", E1, E2, E3),
                    Atom("not_3v", E3, E4),
                ],
                ["E4"],
                [
                    Atom("resolve_name", "magnesium", E1),
                    Atom("resolve_name", "metal", E2),
                    Atom("isa", E1, E2, E3),
                    Atom("not_3v", E3, E4),
                ],
            ],
            # regression test
            [
                [
                    Atom("resolve_name", "Equator", E2),
                    Atom("resolve_name", "Australasia", E3),
                    Atom("not", [Atom("in", E1, E3)]),
                ],
                [],
                [
                    Atom("resolve_name", "Equator", E2),
                    Atom(
                        "scope",
                        [Atom("resolve_name", "Australasia", E3), Atom("scope", [Atom("not", [Atom("in", E1, E3)])])],
                    ),
                ],
            ],
        ]

        for test in tests:
            atoms, root_variables, answer = test
            result = IsolateIndependentParts().isolate(atoms, root_variables)
            self.assertEqual(answer, result)
