from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeProcessor import SomeProcessor
from vrel.core.Solver import Solver
from vrel.interface.SomeSolver import SomeSolver
from vrel.processor.semantic_composer.SemanticComposerProduct import (
    SemanticComposerProduct,
)
from vrel.processor.semantic_executor.AtomExecutorProduct import AtomExecutorProduct


class AtomExecutor(SomeProcessor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """

    composer: SomeProcessor
    model: SomeModel

    def __init__(self, composer: SomeProcessor, model: SomeModel) -> None:
        super().__init__()
        self.composer = composer
        self.model = model

    def get_name(self) -> str:
        return "Executor"

    def process(self, incoming: SemanticComposerProduct, logger: SomeLogger) -> ProcessResult:
        sentences = incoming.sentences

        products = []
        for sentence in sentences:

            solver = Solver(self.model, sentence, logger)

            bindings = solver.solve(sentence.semantics)

            product = AtomExecutorProduct(bindings)

            # todo: is this right?
            products = [product]

        return ProcessResult(products, "")
