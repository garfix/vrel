from vrel.entity import Id
from vrel.entity.Relation import Parameter, Relation
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.interface.SomePronounHandler import SomePronounHandler


class PronounModule(SomeModule, SomePronounHandler):
    """
    This module updates the salience of discource entities, and allows you to check if a pronoun is suitable for generation.
    """

    salience: dict[str, float]

    def __init__(self) -> None:
        super().__init__()

        self.salience = {}

        self.add_relation(
            Relation(
                "unambiguous_pronoun",
                parameters=[Parameter("entity", Id), Parameter("feature", str)],
                query_function=self.unambiguous_pronoun,
            )
        )

    # ('unambiguous_pronoun', entity, feature)
    def unambiguous_pronoun(self, arguments: list, context: ExecutionContext) -> list[list]:

        id, feature = arguments

        print("pronoun?", id, feature)

        return [[None, None]]
