import pathlib
import unittest


from vrel.core.BasicGenerator import BasicGenerator
from vrel.core.BasicSystem import BasicSystem
from vrel.core.DialogTester import DialogTester
from vrel.core.Logger import Logger
from vrel.grammar.en_us_write import get_en_us_write_grammar
from vrel.module.DeductionModule import DeductionModule
from vrel.processor.parser.helper.SimpleGrammarRulesParser import (
    SimpleGrammarRulesParser,
)
from vrel.processor.semantic_composer.SemanticComposer import SemanticComposer
from vrel.processor.semantic_executor.AtomExecutor import AtomExecutor
from vrel.core.Model import Model
from vrel.processor.parser.BasicParser import BasicParser
from vrel.data_source.WikidataDataSource import WikidataDataSource
from .WikidataOutputBuffer import WikidataOutputBuffer
from .WikidataModule import WikidataModule
from .write_grammar import get_write_grammar
from .read_grammar import get_read_grammar


class TestWikiData(unittest.TestCase):
    """
    In this test we connect to Wikidata Query Service, using its SPARQL endpoint

    NB!    Results from Wikidata are cached to file, for speed and to avoid making too many requests

    Set result_cache_path to None to access Wikidata without the cache

    The endpoint is accessed via HTTP, so we need the requests library

    pip install requests

    """

    def test_wikidata(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/"
        result_cache_path = (
            str(pathlib.Path(__file__).parent.resolve()) + "/result_cache/"
        )

        # define the data source
        wikidata = WikidataModule(
            WikidataDataSource(result_cache_path=result_cache_path)
        )

        # define the intents
        # define predicate mapping from the domain to one or more Wikidata predicates

        inferences = DeductionModule()
        inferences.import_rules(path + "mapping.pl")
        inferences.import_rules(path + "intents.pl")

        # a data source to store information for output

        output_buffer = WikidataOutputBuffer()

        # define the model

        model = Model(
            [
                inferences,
                output_buffer,
                wikidata,
            ]
        )

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

        tests = [
            ["Where was madonna born?", "Bay City"],
        ]

        logger.log_no_tests()
        # logger.log_products()

        tester = DialogTester(self, tests, system, logger)
        tester.run()

        print(logger)
