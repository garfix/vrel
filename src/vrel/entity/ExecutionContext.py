from dataclasses import dataclass

from vrel.entity.Relation import Relation
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeSolver import SomeSolver
from vrel.processor.semantic_composer.SemanticSentence import SemanticSentence


@dataclass(frozen=True)
class ExecutionContext:
    relation: Relation
    solver: SomeSolver
    sentence: SemanticSentence
    model: SomeModel
    logger: SomeLogger
