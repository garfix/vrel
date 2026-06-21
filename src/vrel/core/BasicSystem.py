from vrel.core.Solver import Solver
from vrel.core.Logger import Logger
from vrel.entity.Atom import Atom
from vrel.entity.ParseTreeNode import ParseTreeNode
from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeComposer import SomeComposer
from vrel.interface.SomeExecutor import SomeExecutor
from vrel.interface.SomeGenerator import SomeGenerator
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeParser import SomeParser
from vrel.interface.SomeSolver import SomeSolver
from vrel.interface.SomeSystem import SomeSystem
from vrel.processor.semantic_composer.SemanticComposerProduct import SemanticComposerProduct
from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence
from .Model import Model


class BasicSystem(SomeSystem):
    parser: SomeParser
    composer: SomeComposer
    executor: SomeExecutor
    output_generator: SomeGenerator
    model: SomeModel
    logger: SomeLogger

    def __init__(
        self,
        model: SomeModel = None,
        parser: SomeParser = None,
        composer: SomeComposer = None,
        executor: SomeExecutor = None,
        output_generator: SomeGenerator = None,
        logger: SomeLogger = None,
    ):

        self.model = model if model else Model([])
        self.logger = logger if logger else Logger()
        self.parser = parser
        self.composer = composer
        self.executor = executor
        self.output_generator = output_generator

    def get_logger(self) -> SomeLogger:
        return self.logger

    def enter(self, request: SentenceRequest) -> ProcessResult | None:
        if not self.parser:
            return None

        solver = Solver(self.model, request, self.logger)

        return self.parse(request, solver)

    def parse(self, request: SentenceRequest, solver: SomeSolver):

        parse_result = self.parser.process(request.text, self.logger)
        if parse_result.error_type != "":
            return self.log_error(parse_result, solver)

        if not self.composer:
            return parse_result

        for parse_product in parse_result.products:
            # each result is an ambiguous alternative
            result = self.compose(parse_product.parse_trees, request, solver)
            if result is not None:
                return result

        return None

    def compose(self, parse_trees: list[ParseTreeNode], request: SentenceRequest, solver: SomeSolver):
        """
        Note: these parse trees all belong to the same input; they're not alternative parses
        """

        sentences = []
        for parse_tree in parse_trees:
            sentences.append(self.composer.process(parse_tree, self.logger))

        product = SemanticComposerProduct(sentences)

        if not self.executor:
            return ProcessResult([product], "")

        result = self.execute(sentences, request, solver)
        if result is not None:
            return result

        return None

    def execute(self, semantic_sentences: list[SemanticSentence], request: SentenceRequest, solver: SomeSolver):
        """
        Note: these sentences all belong to the same input; they're not alternative parses
        """

        products = []
        for semantic_sentence in semantic_sentences:
            product = self.executor.process(semantic_sentence, solver, request, self.logger)
            products.append(product)

        return ProcessResult(products, "")

    def log_error(self, result: ProcessResult, solver: SomeSolver):
        solver.write_atom(Atom("output_type", result.error_type))
        solver.write_atom(Atom("output_" + result.error_type, *result.error_args))
        return result

    def read_output(self):
        return self.output_generator.generate_output()
