from vrel.core.Solver import Solver
from vrel.core.Logger import Logger
from vrel.entity.Atom import Atom
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
from vrel.processor.parser.BasicParserProduct import BasicParserProduct
from vrel.processor.semantic_composer.SemanticComposerProduct import SemanticComposerProduct
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
            result = self.compose(parse_product, request, solver)
            if result is not None:
                return result

        return None

    def compose(self, parse_product: BasicParserProduct, request: SentenceRequest, solver: SomeSolver):

        composer_result = self.composer.process(parse_product.parse_trees, self.logger)
        if composer_result.error_type != "":
            return self.log_error(composer_result)

        if not self.executor:
            return composer_result

        for composer_product in composer_result.products:
            result = self.execute(composer_product, request, solver)
            if result is not None:
                return result

        return None

    def execute(self, composer_product: SemanticComposerProduct, request: SentenceRequest, solver: SomeSolver):

        executor_result = self.executor.process(composer_product.sentences, solver, request, self.logger)
        if executor_result.error_type != "":
            return self.log_error(executor_result, solver)

        return executor_result

    def log_error(self, result: ProcessResult, solver: SomeSolver):
        solver.write_atom(Atom("output_type", result.error_type))
        solver.write_atom(Atom("output_" + result.error_type, *result.error_args))
        return result

    def read_output(self):
        return self.output_generator.generate_output()
