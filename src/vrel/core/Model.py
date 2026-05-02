from vrel.entity.Relation import Relation
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeModule import SomeModule
from vrel.interface.SomeSameAsHandler import SomeSameAsHandler
from vrel.interface.SomeStackOverflowHandler import SomeStackOverflowHandler
from vrel.core.handlers.NoStackOverflowHandler import NoStackOverflowHandler
from vrel.module.CoreModule import CoreModule


class Model(SomeModel):
    """
    This class represents the generic part of the model.
    """

    modules: list[SomeModule]
    same_as_handler: SomeSameAsHandler | None
    stack_overflow_handler: SomeStackOverflowHandler | None

    def __init__(
        self,
        modules: list[SomeModule],
        same_as_handler: SomeSameAsHandler = None,
        stack_overflow_handler: SomeStackOverflowHandler = None,
    ) -> None:
        self.modules = [
            CoreModule(),
        ]
        self.modules.extend(modules)

        self.same_as_handler = same_as_handler
        if self.same_as_handler:
            self.same_as_handler.model = self

        if stack_overflow_handler:
            self.stack_overflow_handler = stack_overflow_handler
        else:
            self.stack_overflow_handler = NoStackOverflowHandler()

    def get_same_as_handler(self) -> SomeSameAsHandler | None:
        return self.same_as_handler

    def get_stack_overflow_handler(self) -> SomeStackOverflowHandler | None:
        return self.stack_overflow_handler

    def find_relations(self, predicate: str) -> list[Relation]:
        result = []
        for module in self.modules:
            relation = module.get_relation(predicate)
            if relation:
                result.append(relation)

        return result
