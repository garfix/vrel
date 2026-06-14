from vrel.entity.Relation import Relation
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeModule import SomeModule
from vrel.interface.SomeSameAsHandler import SomeSameAsHandler
from vrel.interface.SomeStackOverflowHandler import SomeStackOverflowHandler
from vrel.core.handlers.NoStackOverflowHandler import NoStackOverflowHandler
from vrel.module.CoreModule import CoreModule
from vrel.module.SameAsModule import DummySameAsHandler
from vrel.processor.semantic_composer.helper.VariableGenerator import VariableGenerator


class Model(SomeModel):
    """
    This class represents the generic part of the model.
    """

    modules: list[SomeModule]
    dialog_constant_generator: VariableGenerator
    same_as_handler: SomeSameAsHandler
    stack_overflow_handler: SomeStackOverflowHandler | None

    def __init__(
        self,
        modules: list[SomeModule],
        stack_overflow_handler: SomeStackOverflowHandler = None,
    ) -> None:
        self.modules = [
            CoreModule(),
        ]

        self.same_as_handler = DummySameAsHandler()

        for module in modules:
            self.modules.append(module)
            if isinstance(module, SomeSameAsHandler):
                self.same_as_handler = module
                # todo: fix this hack
                module.model = self

        if stack_overflow_handler:
            self.stack_overflow_handler = stack_overflow_handler
        else:
            self.stack_overflow_handler = NoStackOverflowHandler()

        self.dialog_constant_generator = VariableGenerator("DLG")

    def get_dialog_constant_generator(self) -> VariableGenerator:
        return self.dialog_constant_generator

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
