from vrel.entity.ProcessResult import ProcessResult
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeExecutor import SomeExecutor
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeSolver import SomeSolver
from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence
from vrel.processor.semantic_executor.helper.resolve_constants import resolve_constants
from vrel.processor.semantic_executor.helper.resolve_names import resolve_names
from vrel.processor.semantic_executor.AtomExecutorProduct import AtomExecutorProduct


class AtomExecutor(SomeExecutor):
    """
    Executes the function that forms the meaning of the sentence, and produces its result
    """

    def __init__(self) -> None:
        super().__init__()

    def process(
        self,
        semantic_sentence: SemanticSentence,
        solver: SomeSolver,
        request: SentenceRequest,
        logger: SomeLogger,
    ) -> ProcessResult:

        request.semantic_sentence = semantic_sentence

        semantics = [semantic_sentence.semantics]
        resolved_constants = resolve_constants(semantics)
        resolved_names = resolve_names(resolved_constants, solver)

        logger.add_section("Names resolved", resolved_names)

        bindings = solver.solve(resolved_names)

        logger.add_section("Result bindings", "\n".join(str(d) for d in bindings))

        product = AtomExecutorProduct(bindings)
        return product
