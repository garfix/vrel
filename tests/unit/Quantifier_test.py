import sqlite3
import unittest

from vrel.core.BasicSystem import BasicSystem
from vrel.core.Model import Model
from vrel.core.constants import E1, E2, Body, Range
from vrel.data_source.Sqlite3DataSource import Sqlite3DataSource
from vrel.entity.Atom import Atom
from vrel.entity.Relation import Relation
from vrel.interface.SomeDataSource import SomeDataSource
from vrel.interface.SomeModule import SomeModule
from vrel.processor.parser.helper.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from vrel.processor.parser.helper.grammar_functions import apply
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.processor.parser.BasicParser import BasicParser
from vrel.processor.semantic_composer.SemanticComposer import SemanticComposer
from vrel.processor.semantic_executor.AtomExecutor import AtomExecutor
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.SemanticFunction import SemanticFunction


class SimpleModule(SomeModule):
    ds: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("parent", query_function=self.parent))
        self.add_relation(Relation("child", query_function=self.child))
        self.add_relation(Relation("have", query_function=self.have))

    def parent(self, arguments: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("has_child", ["parent"], arguments)
        return out_values

    def child(self, arguments: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("has_child", ["child"], arguments)
        return out_values

    def have(self, arguments: list, context: ExecutionContext) -> list[list]:
        out_values = self.ds.select("has_child", ["parent", "child"], arguments)
        return out_values


class TestQuantification(unittest.TestCase):

    def test_quantification(self):

        connection = sqlite3.connect(":memory:")
        cursor = connection.cursor()
        data_source = Sqlite3DataSource(connection)

        # note: same entity may have multiple names
        cursor.execute("CREATE TABLE has_child (parent TEXT, child TEXT)")

        data_source.insert("has_child", ["parent", "child"], ["mary", "lucy"])
        data_source.insert("has_child", ["parent", "child"], ["mary", "bonny"])
        data_source.insert("has_child", ["parent", "child"], ["barbara", "john"])
        data_source.insert("has_child", ["parent", "child"], ["barbara", "chuck"])
        data_source.insert("has_child", ["parent", "child"], ["william", "oswald"])
        data_source.insert("has_child", ["parent", "child"], ["william", "bertrand"])

        model = Model([SimpleModule(data_source)])

        simple_grammar = [
            {"syn": "s(V1) -> np(E1) verb(V1) np(E2)", "sem": lambda np1, verb, np2: Atom(verb, np1, np2)},
            {"syn": "verb(E1, E2) -> 'has'", "sem": lambda: [("have", E1, E2)]},
            {
                "syn": "np(E1) -> det(E1) nbar(E1)",
                "sem": lambda det, nbar: nbar.addArguments(det),
            },
            {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: Atom(E1, noun)},
            {"syn": "det(E1) -> 'every'", "sem": lambda: {"determiner": "all"}},
            {
                "syn": "det(E1) -> number(E1)",
                "sem": lambda number: {"determiner": number},
            },
            {"syn": "number(D1) -> 'two'", "sem": lambda: 2},
            {"syn": "number(D1) -> 'three'", "sem": lambda: 3},
            {"syn": "noun(E1) -> 'parent'", "sem": lambda: [("parent", E1)]},
            {"syn": "noun(E1) -> 'children'", "sem": lambda: [("child", E1)]},
        ]

        grammar = SimpleGrammarRulesParser().parse_read_grammar(simple_grammar)
        parser = BasicParser(grammar)
        composer = SemanticComposer(parser)
        executor = AtomExecutor(composer, model)

        system = BasicSystem(
            model=model,
            parser=parser,
            composer=composer,
            executor=executor,
        )

        request = SentenceRequest("Every parent has two children")
        response = system.enter(request)
        self.assertEqual(len(response.products[0].bindings), 3)

        request = SentenceRequest("Every parent has three children")
        response = system.enter(request)
        self.assertEqual(len(response.products[0].bindings), 0)
