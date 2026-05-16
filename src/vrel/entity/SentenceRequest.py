from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence


class SentenceRequest:

    # raw text that serves as the input to the request
    text: str

    # this sentence is updated during the handling of the request
    semantic_sentence: SemanticSentence

    def __init__(self, text: str) -> None:
        self.text = text
