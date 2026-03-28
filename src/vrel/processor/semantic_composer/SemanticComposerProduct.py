from dataclasses import dataclass
from vrel.core.Logger import Logger
from vrel.interface.SomeProduct import SomeProduct
from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence

@dataclass(frozen=True)
class SemanticComposerProduct(SomeProduct):
    sentences: list[SemanticSentence]

    def log(self, logger: Logger):
        for sentence in self.sentences:
            sentence.log(logger)


    def get_output(self) -> any:
        return list(map(lambda s: s.semantics, self.sentences))

