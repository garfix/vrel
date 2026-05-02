import unittest

from vrel.core.BasicGenerator import BasicGenerator
from vrel.core.BasicSystem import BasicSystem
from vrel.core.Model import Model
from vrel.core.Solver import Solver
from vrel.core.constants import E1
from vrel.entity.Atom import Atom
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.module.BasicOutputBuffer import BasicOutputBuffer
from vrel.processor.parser.BasicParser import BasicParser
from vrel.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from vrel.processor.semantic_composer.SemanticComposer import SemanticComposer
from vrel.processor.semantic_executor.AtomExecutor import AtomExecutor
from atom_executor.write_grammar import get_write_grammar
from atom_executor.AtomExecutorDialogContext import AtomExecutorDialogContext
from atom_executor.SimpleModule import SimpleModule


class TestAtomExecutor(unittest.TestCase):

    def test_produce_exception_output(self):
        """
        resolve_name fails to find "John" and produces output
        It's error is passed to the ProcessingResult and the BlockResult
        and ends up in the response
        """

        read_grammar = [
            {"syn": "s(E1) -> noun(E1) verb(V)", "sem": lambda noun, verb: noun + verb},
            {"syn": "noun(E1) -> proper_noun(E1)", "sem": lambda proper_noun: [Atom("resolve_name", proper_noun, E1)]},
            {"syn": "proper_noun(E1) -> /\\w+/", "sem": lambda token: token},
            {"syn": "verb(E1) -> 'walks'", "sem": lambda: [Atom("walks", E1)]},
        ]

        facts = SimpleModule()
        output_buffer = BasicOutputBuffer()

        model = Model(
            [
                facts,
                output_buffer,
            ]
        )

        solver = Solver(model)

        read_grammar = SimpleGrammarRulesParser().parse_read_grammar(read_grammar)
        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(get_write_grammar())
        parser = BasicParser(read_grammar)
        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, model)
        generator = BasicGenerator(write_grammar, model, output_buffer)

        system = BasicSystem(
            model=model, parser=parser, composer=composer, executor=executor, output_generator=generator
        )

        system.enter(SentenceRequest("John walks"))
        output = generator.generate_output()

        self.assertEqual("Name not found: john", output)

    # def test_inferences(self):
    #     """
    #     Contains an inference that stores an atom in a data store
    #     Contains executable code that stores an atom in a data store
    #     """

    #     simple_grammar = [
    #         {"syn": "s(E1) -> noun(E1) 'be'", "sem": lambda noun: noun},
    #         {
    #             "syn": "s(E1) -> /\\w+/ 'exist'",
    #             "sem": lambda token: [],
    #         },
    #         {
    #             "syn": "noun(E1) -> 'continents'",
    #             "sem": lambda: [Atom("continent", E1)],
    #             "dialog": [Atom("isa", e1, "continent")],
    #         },
    #     ]

    #     facts = SimpleModule()
    #     dialog_context = AtomExecutorDialogContext()

    #     model = Model([facts, dialog_context])

    #     grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
    #     parser = BasicParser(grammar)
    #     composer = SemanticComposer(parser)
    #     executor = AtomExecutor(composer, model)

    #     system = BasicSystem(model=model, parser=parser, composer=composer, executor=executor)

    #     # test the inference
    #     system.enter(SentenceRequest("Continents be"))
    #     results = dialog_context.data_source.select("isa", ["entity", "type"], [Variable("E1"), Variable("E2")])
    #     self.assertEqual(["$1", "continent"], results[0])
