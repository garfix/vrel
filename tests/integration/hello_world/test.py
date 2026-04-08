import unittest
import pathlib

from vrel.core.BasicGenerator import BasicGenerator
from vrel.core.BasicSystem import BasicSystem
from vrel.core.DialogTester import DialogTester
from vrel.core.Logger import Logger
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.grammar.en_us_write import get_en_us_write_grammar
from vrel.module.BasicDialogContext import BasicDialogContext
from vrel.module.BasicOutputBuffer import BasicOutputBuffer
from vrel.processor.parser.helper.SimpleGrammarRulesParser import (
    SimpleGrammarRulesParser,
)
from vrel.processor.semantic_composer.SemanticComposer import SemanticComposer
from vrel.processor.semantic_executor.AtomExecutor import AtomExecutor
from vrel.core.Model import Model
from vrel.processor.parser.BasicParser import BasicParser
from vrel.module.DeductionModule import DeductionModule
from .HelloWorldDB import HellowWorldDB
from .HelloWorldModule import HelloWorldModule
from .read_grammar import get_read_grammar
from .write_grammar import get_write_grammar


class TestHelloWorld(unittest.TestCase):
    """
    A basic application that creates a test and shows how to interact with the system.
    """

    def test_hello_world(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/"

        # define the database

        db = HellowWorldDB()
        facts = HelloWorldModule(db)

        # define the intents and other inferences

        inferences = DeductionModule()
        inferences.import_rules(path + "inferences.pl")
        inferences.import_rules(path + "intents.pl")

        # a data source to store information for output

        output_buffer = BasicOutputBuffer()
        dialog_context = BasicDialogContext()

        # define the model

        model = Model([facts, inferences, output_buffer, dialog_context])

        # define the pipeline

        read_grammar = SimpleGrammarRulesParser().parse_read_grammar(get_read_grammar())
        parser = BasicParser(read_grammar)

        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, model)

        write_grammar = SimpleGrammarRulesParser().parse_write_grammar(
            get_en_us_write_grammar() + get_write_grammar()
        )
        generator = BasicGenerator(write_grammar, model, output_buffer)

        logger = Logger()

        # define the system

        system = BasicSystem(
            model=model,
            parser=parser,
            composer=composer,
            executor=executor,
            output_generator=generator,
            logger=logger,
        )

        # test the system

        tests = [
            ["Hello world", "Hi there!"],
            [
                "What rivers are there?",
                "amazon, amu_darya, amur, brahmaputra, colorado, congo_river, cubango, danube, don, elbe, euphrates, ganges, hwang_ho, indus, irrawaddy, lena, limpopo, mackenzie, mekong, mississippi, murray, niger_river, nile, ob, oder, orange, orinoco, parana, rhine, rhone, rio_grande, salween, senegal_river, tagus, vistula, volga, volta, yangtze, yenisei, yukon, zambesi",
            ],
        ]

        # comment in the following rules to see intermediate results

        logger.log_no_tests()
        # logger.log_all_tests()
        # logger.log_products()

        tester = DialogTester(self, tests, system, logger)
        tester.run()

        print(logger)

        # how to actually use the system

        system.enter(SentenceRequest("Hello world"))
        output = system.read_output()
        # print(output)
