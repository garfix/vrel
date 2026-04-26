import unittest

from vrel.core.BasicSystem import BasicSystem
from vrel.core.Model import Model
from vrel.core.Solver import Solver
from vrel.core.constants import E1
from vrel.entity.Atom import Atom
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.processor.parser.BasicParser import BasicParser
from vrel.processor.parser.helper.SimpleGrammarRulesParser import (
    SimpleGrammarRulesParser,
)
from vrel.processor.semantic_composer.SemanticComposer import SemanticComposer
from vrel.processor.semantic_executor.AtomExecutor import AtomExecutor


class TestComposer(unittest.TestCase):

    def test_missing_sem(self):
        simple_grammar = [
            {
                "syn": "s(E1) -> proper_noun(E1) verb(V)",
                "sem": lambda proper_noun, verb: proper_noun + verb,
            },
            {"syn": "proper_noun(E1) -> 'mary'"},
            {"syn": "verb(E1) -> 'walks'"},
        ]

        model = Model([])
        solver = Solver(model)
        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, model, solver)

        system = BasicSystem(model=model, parser=parser, composer=composer, executor=executor)

        exception_occurred = False
        try:
            system.enter(SentenceRequest("Mary walks"))
        except Exception as e:
            self.assertEqual(str(e), "Rule 'proper_noun(E1) -> 'mary'' is missing key 'sem'")
            exception_occurred = True

        self.assertEqual(exception_occurred, True)

    def test_variable_unification(self):

        simple_grammar = [
            {
                "syn": "s(E1) -> np(E2) verb(E2, E3) np(E3)",
                "sem": lambda np1, verb, np2: Atom(verb, np1, np2),
            },
            {"syn": "verb(E1, E2) -> 'flows' 'to'", "sem": lambda: "flows"},
            {
                "syn": "np(E1) -> det(E1) nbar(E1)",
                "sem": lambda det, nbar: nbar.any([det]),
            },
            {"syn": "det(E1) -> 'the'", "sem": lambda: Atom("quantifier" "the")},
            {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: Atom(noun, E1)},
            {"syn": "noun(E1) -> 'river'", "sem": lambda: "river"},
            {"syn": "noun(E1) -> 'sea'", "sem": lambda: "sea"},
        ]

        model = Model([])
        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)

        system = BasicSystem(
            model=model,
            parser=parser,
            composer=composer,
        )

        request = SentenceRequest("The river flows to the sea")
        response = system.enter(request)

        semantics = response.products[0].sentences[0].semantics
        # todo

    def test_special_category(self):

        simple_grammar = [
            {"syn": "s(V) -> np(E1) 'sleeps'", "sem": lambda np: np},
            {
                "syn": "np(E1) -> proper_noun(E1)",
                "sem": lambda proper_noun: proper_noun,
            },
            {"syn": "proper_noun(E1) -> /\\w+/", "sem": lambda token: token},
            {"syn": "proper_noun(E1) -> /\\w+ \\w+/", "sem": lambda token: token},
        ]

        model = Model([])
        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)

        system = BasicSystem(model=model, parser=parser)

        # two tokens

        system = BasicSystem(model=model, parser=parser, composer=composer)

        request = SentenceRequest("John Walker sleeps")
        response = system.enter(request)
        self.assertEqual(str(response.products[0].sentences[0].semantics), "John Walker")

    def test_multiple_root_variables(self):

        simple_grammar = [
            {"syn": "s(E1, E2) -> np(E1) vp(E2)", "sem": lambda np, vp: np + vp},
            {"syn": "np(E1) -> 'john'", "sem": lambda: "john"},
            {"syn": "vp(E1) -> 'sleeps'", "sem": lambda: "sleeps"},
        ]

        model = Model([])
        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)

        system = BasicSystem(
            model=model,
            parser=parser,
            composer=composer,
        )

        request = SentenceRequest("John sleeps")
        product = system.enter(request)
        self.assertEqual(product.products[0].sentences[0].root_variables, ["$1", "$2"])

    def test_regexp(self):

        simple_grammar = [
            {"syn": "s(V) -> 'does' np(E1) 'sleep'~'?'", "sem": lambda np: np},
            {
                "syn": "np(E1) -> proper_noun(E1)",
                "sem": lambda proper_noun: proper_noun,
            },
            {"syn": "proper_noun(E1) -> /\\w+/", "sem": lambda token: token},
        ]

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)

        system = BasicSystem(
            model=Model([]),
            parser=parser,
            composer=composer,
        )

        # basic

        request = SentenceRequest("Does John sleep?")
        response = system.enter(request)

        # product: BasicParserProduct = request.get_current_product(parser)
        self.assertEqual(str(response.products[0].sentences[0].semantics), "John")
