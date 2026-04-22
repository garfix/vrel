import sqlite3
import unittest

from vrel.core.BasicSystem import BasicSystem
from vrel.core.Model import Model
from vrel.core.constants import ARG_DETERMINER, E1, E3
from vrel.data_source.Sqlite3DataSource import Sqlite3DataSource
from vrel.entity.Atom import Atom
from vrel.entity.Relation import Relation
from vrel.interface.SomeDataSource import SomeDataSource
from vrel.interface.SomeModule import SomeModule
from vrel.processor.parser.helper.SimpleGrammarRulesParser import (
    SimpleGrammarRulesParser,
)
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.processor.parser.BasicParser import BasicParser
from vrel.processor.semantic_composer.SemanticComposer import SemanticComposer
from vrel.processor.semantic_executor.AtomExecutor import AtomExecutor
from vrel.entity.ExecutionContext import ExecutionContext


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

        def have(det: Atom, nbar: Atom):
            return nbar.mod(Atom(ARG_DETERMINER, [det]))

        simple_grammar = [
            {
                "syn": "s() -> np(E1) verb(E1, E2) np(E2)",
                "sem": lambda np1, verb, np2: [
                    Atom("create_query", [Atom(verb, np1, np2)], E3),
                    Atom("scoped", E3),
                ],
            },
            {"syn": "verb(E1, E2) -> 'has'", "sem": lambda: "have"},
            {
                "syn": "np(E1) -> det(E1) nbar(E1)",
                "sem": lambda det, nbar: nbar.with_determiner(det),
            },
            {"syn": "nbar(E1) -> noun(E1)", "sem": lambda noun: noun},
            {"syn": "det(E1) -> 'every'", "sem": lambda: Atom("all")},
            {
                "syn": "det(E1) -> number(E1)",
                "sem": lambda number: Atom("equals", number),
            },
            {"syn": "number(D1) -> 'two'", "sem": lambda: 2},
            {"syn": "number(D1) -> 'three'", "sem": lambda: 3},
            {"syn": "noun(E1) -> 'parent'", "sem": lambda: Atom("parent", E1)},
            {"syn": "noun(E1) -> 'children'", "sem": lambda: Atom("child", E1)},
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
