import pathlib
import unittest


from vrel.core.BasicGenerator import BasicGenerator
from vrel.core.BasicSystem import BasicSystem
from vrel.core.DialogTester import DialogTester
from vrel.grammar.en_us_write import get_en_us_write_grammar
from vrel.module.DeductionModule import DeductionModule
from vrel.processor.semantic_composer.SemanticComposer import SemanticComposer
from vrel.processor.semantic_executor.AtomExecutor import AtomExecutor
from vrel.core.Model import Model
from vrel.processor.parser.BasicParser import BasicParser
from vrel.data_source.WikidataDataSource import WikidataDataSource
from WikidataModule import WikidataModule
from write_grammar import get_write_grammar
from read_grammar import get_read_grammar


class TestWikiData(unittest.TestCase):
    """
    In this test we connect to Wikidata Query Service, using its SPARQL endpoint

    NB!    Results from Wikidata are cached to file, for speed and to avoid making too many requests

    Set result_cache_path to None to access Wikidata without the cache

    The endpoint is accessed via HTTP, so we need the requests library

    pip install requests

    """

    def test_wikidata(self):

        path = pathlib.Path(__file__).parent
        result_cache_path = path / "result_cache"

        # define the data source
        wikidata = WikidataModule(WikidataDataSource(result_cache_path=result_cache_path))

        # define the intents
        # define predicate mapping from the domain to one or more Wikidata predicates

        inferences = DeductionModule()
        inferences.import_rules(path / "mapping.pl")
        inferences.import_rules(path / "intents.pl")

        # define the model

        model = Model(
            [
                inferences,
                wikidata,
            ]
        )

        # define the pipeline

        parser = BasicParser()
        parser.add_grammar_rules(get_read_grammar())

        composer = SemanticComposer()
        executor = AtomExecutor()

        generator = BasicGenerator(model)
        generator.add_grammar_rules(get_en_us_write_grammar())
        generator.add_grammar_rules(get_write_grammar())

        # define the system

        system = BasicSystem(
            model=model,
            parser=parser,
            composer=composer,
            executor=executor,
            output_generator=generator,
        )

        tests = [
            ["Where was madonna born?", "Bay City"],
        ]

        tester = DialogTester(self, tests, system)
        tester.run()
