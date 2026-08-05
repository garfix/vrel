import re
from vrel.entity.Grammar import Grammar
from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.SimpleGrammar import SimpleGrammar
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeParseTreeSortHeuristics import SomeParseTreeSortHeuristics
from vrel.interface.SomeParser import SomeParser
from vrel.processor.parser.BasicParserProduct import BasicParserProduct
from vrel.dsl.SimpleGrammarRulesParser import SimpleGrammarRulesParser
from vrel.processor.parser.helper.sentence_extractor import extract_sentences
from .tree_sort_heuristics.BasicParseTreeSortHeuristics import BasicParseTreeSortHeuristics
from .earley.EarleyParser import EarleyParser


class BasicParser(SomeParser):

    grammar: Grammar
    parser: EarleyParser
    tree_sorter: SomeParseTreeSortHeuristics
    sentence_categories: str

    def __init__(self, sentence_categories=["s"]) -> None:
        self.parser = EarleyParser()
        self.tree_sorter = BasicParseTreeSortHeuristics()
        self.sentence_categories = sentence_categories
        self.grammar = Grammar([])

    def add_grammar_rules(self, rules: SimpleGrammar):
        SimpleGrammarRulesParser().parse_read_grammar(rules, self.grammar)

    def process(self, input: str, logger: SomeLogger) -> ProcessResult:
        # replace whitespace sequences by single space
        source_text = re.sub("\\s+", " ", input)

        result = self.parser.parse(self.grammar, source_text)

        sorted_trees = self.tree_sorter.sort_trees(result.products)

        products = []
        for tree in sorted_trees:
            sentence_trees = extract_sentences(tree, self.sentence_categories)
            if len(sentence_trees) > 0:
                products.append(BasicParserProduct(sentence_trees))

                # for tree in sentence_trees:
                #     logger.add_section("Syntax tree", tree)

        return ProcessResult(products, result.error_type, result.error_args)
