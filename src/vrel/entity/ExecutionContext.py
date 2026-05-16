from dataclasses import dataclass

from vrel.entity.Relation import Relation
from vrel.entity.SentenceRequest import SentenceRequest
from vrel.interface.SomeLogger import SomeLogger
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeSolver import SomeSolver


@dataclass(frozen=True)
class ExecutionContext:
    relation: Relation
    solver: SomeSolver
    request: SentenceRequest
    model: SomeModel
    logger: SomeLogger
