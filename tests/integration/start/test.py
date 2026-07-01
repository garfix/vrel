import pathlib
import sqlite3
import unittest

from StartModule import StartModule
from vrel.core.BasicGenerator import BasicGenerator
from vrel.core.BasicSystem import BasicSystem
from vrel.core.DialogTester import DialogTester
from vrel.data_source.Sqlite3DataSource import Sqlite3DataSource
from vrel.grammar.en_us_write import get_en_us_write_grammar
from vrel.module.BasicOutputBuffer import BasicOutputBuffer
from vrel.processor.semantic_composer.SemanticComposer import SemanticComposer
from vrel.processor.semantic_executor.AtomExecutor import AtomExecutor
from vrel.core.Model import Model
from vrel.processor.parser.BasicParser import BasicParser
from vrel.module.DeductionModule import DeductionModule
from write_grammar import get_write_grammar
from read_grammar import get_read_grammar

tests = [
    [
        "What rivers are there?",
        "amazon, amu_darya, amur, brahmaputra, colorado, congo_river, cubango, danube, don, elbe, euphrates, ganges, hwang_ho, indus, irrawaddy, lena, limpopo, mackenzie, mekong, mississippi, murray, niger_river, nile, ob, oder, orange, orinoco, parana, rhine, rhone, rio_grande, salween, senegal_river, tagus, vistula, volga, volta, yangtze, yenisei, yukon, zambesi",
    ],
    [
        "Bye",
        "See you later!",
    ],
]


class StartTest(unittest.TestCase):

    def test_chat80(self):

        path = pathlib.Path(__file__).parent

        # define the data source

        connection = sqlite3.connect(":memory:")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE employee (id INT PRIMARY KEY, name TEXT, birth_date DATE)")
        cursor.execute("INSERT INTO employee (id, name, birth_date) VALUES (1, 'Patrick', '1969-11-24')")
        cursor.execute("INSERT INTO employee (id, name, birth_date) VALUES (2, 'Jackie', '1984-02-12')")
        cursor.execute("INSERT INTO employee (id, name, birth_date) VALUES (3, 'Barbara', '1962-07-30')")
        cursor.execute("INSERT INTO employee (id, name, birth_date) VALUES (4, 'Billy', '2003-01-15')")

        db = Sqlite3DataSource(connection)

        # define the module

        facts = StartModule(db)

        # define the decution rules

        inferences = DeductionModule()
        inferences.import_rules(path / "intents.pl")
        # inferences.import_rules(path / "inferences.pl")

        # define the model

        output_buffer = BasicOutputBuffer()
        model = Model([facts, inferences, output_buffer])

        # define the parser

        parser = BasicParser()
        parser.add_grammar_rules(get_read_grammar())

        # composer = SemanticComposer()
        # executor = AtomExecutor()

        # generator = BasicGenerator(model, output_buffer)
        # generator.add_grammar_rules(get_en_us_write_grammar())
        # generator.add_grammar_rules(get_write_grammar())

        # # define the system

        # system = BasicSystem(
        #     model=model,
        #     parser=parser,
        #     composer=composer,
        #     executor=executor,
        #     output_generator=generator,
        # )

        # tester = DialogTester(self, tests, system)
        # tester.run()
