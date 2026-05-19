from dataclasses import dataclass
from vrel.interface.SomeProduct import SomeProduct
from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence


@dataclass(frozen=True)
class SemanticComposerProduct(SomeProduct):
    sentences: list[SemanticSentence]

    def get_output(self) -> any:
        return list(map(lambda s: s.semantics, self.sentences))
