from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeProcessor import SomeProcessor
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

    def __init__(self) -> None:
        super().__init__()

    def get_name(self) -> str:
        return "Executor"

    def process(
        self, incoming: SemanticComposerProduct, solver: SomeSolver, request: SentenceRequest, logger: SomeLogger
    ) -> ProcessResult:
        sentences = incoming.sentences

        products = []
        for sentence in sentences:

            request.semantic_sentence = sentence

            semantics = [sentence.semantics]
            resolved_constants = resolve_constants(semantics)
            resolved_names = resolve_names(resolved_constants, solver)

            logger.add_section("Names resolved", resolved_names)

            bindings = solver.solve(resolved_names)

            logger.add_section("Result bindings", "\n".join(str(d) for d in bindings))

            product = AtomExecutorProduct(bindings)
            products.append(product)

        return ProcessResult(products, "")
