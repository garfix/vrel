from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeProcessor import SomeProcessor
from vrel.core.Solver import Solver
from vrel.interface.SomeSolver import SomeSolver
from vrel.processor.semantic_executor.helper.resolve_constants import resolve_constants
from vrel.processor.semantic_executor.helper.resolve_names import resolve_names
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

    def process(self, incoming: SemanticComposerProduct, solver: SomeSolver, request: SentenceRequest) -> ProcessResult:
        sentences = incoming.sentences

        products = []
        for sentence in sentences:

            request.semantic_sentence = sentence

            semantics = [sentence.semantics]
            resolved_constants = resolve_constants(semantics)
            resolved_names = resolve_names(resolved_constants, solver)

            bindings = solver.solve(resolved_names)

            product = AtomExecutorProduct(bindings, resolved_names)
            products.append(product)
            break

        return ProcessResult(products, "")
