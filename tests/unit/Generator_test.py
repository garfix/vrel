import pathlib
import unittest

from vrel.core.BasicGenerator import BasicGenerator
from vrel.core.Model import Model
from vrel.core.Solver import Solver
from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom
from vrel.module.DeductionModule import DeductionModule
from vrel.processor.parser.helper.SimpleGrammarRulesParser import (
    SimpleGrammarRulesParser,
)
from generator.SimpleModuleOutputBuffer import SimpleOutputBuffer


class TestGenerator(unittest.TestCase):

    def test_generator(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/generator/"

        output_buffer = SimpleOutputBuffer()

        inferences = DeductionModule()
        inferences.import_rules(path + "inferences.pl")

        model = Model([inferences, output_buffer])

        raw_grammar = [
            {"syn": "s() -> 'OK'", "if": [Atom("output_type", "ok")]},
            {
                "syn": "s() -> 'The above sentence is impossible'",
                "if": [Atom("output_type", "impossible")],
            },
            {
                "syn": "s() -> np(E2) vp(E1)",
                "if": [
                    Atom("output_type", "declarative"),
                    Atom("output_subject", E1, E2),
                ],
            },
            {
                "syn": "s() -> named_number(E1)",
                "if": [Atom("output_type", "scalar"), Atom("output_value", E1)],
            },
            {"syn": "vp(E1) -> verb(E1) np(E2)", "if": [Atom("output_object", E1, E2)]},
            {"syn": "np(E1) -> text(E2)", "if": [Atom("resolve_name", E2, E1)]},
            {
                "syn": "verb(E1) -> 'married'",
                "if": [Atom("output_predicate", E1, "marry")],
            },
            {"syn": "named_number(E1) -> 'one'", "if": [Atom("equals", E1, 1)]},
            {"syn": "named_number(E1) -> 'two'", "if": [Atom("equals", E1, 2)]},
        ]

        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(raw_grammar)
        generator = BasicGenerator(write_grammar, model, output_buffer)

        tests = [
            {"atoms": [Atom("output_type", "ok")], "output": "OK"},
            {
                "atoms": [Atom("output_type", "impossible")],
                "output": "The above sentence is impossible",
            },
            {
                "atoms": [
                    Atom("output_type", "declarative"),
                    Atom("output_predicate", "5", "marry"),
                    Atom("output_subject", "5", "10892"),
                    Atom("output_object", "5", "37216"),
                ],
                "output": "Jane married John",
            },
            {
                "atoms": [Atom("output_type", "scalar"), Atom("output_value", 2)],
                "output": "two",
            },
        ]

        solver = Solver(model)

        for test in tests:
            output_buffer.clear()
            for atom in test["atoms"]:
                solver.write_atom(atom)
            output = generator.generate_output()
            self.assertEqual(output, test["output"])
