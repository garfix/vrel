from vrel.entity.Id import Id
from vrel.entity.Atom import Atom
from vrel.entity.Relation import Parameter, Relation
from vrel.interface.SomeModule import SomeModule
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.interface.SomePronounHandler import SomePronounHandler
from vrel.module.pronoun.saliency import (
    EntityData,
    check_pronoun,
    decay_saliency,
    process_atoms,
    update_features,
    update_saliency,
)


class PronounModule(SomeModule, SomePronounHandler):
    """
    This module updates the salience of discource entities, and allows you to check if a pronoun is suitable for generation.
    """

    entities: list[EntityData]

    def __init__(self) -> None:
        super().__init__()

        self.entities = []

        self.add_relation(
            Relation(
                "update_saliency",
                parameters=[Parameter("atoms", list[Atom])],
                query_function=self.update_saliency,
            )
        )

        self.add_relation(
            Relation(
                "unambiguous_pronoun",
                parameters=[Parameter("entity", Id), Parameter("feature", str)],
                query_function=self.unambiguous_pronoun,
            )
        )

    # ('unambiguous_pronoun', entity, features)
    def unambiguous_pronoun(self, arguments: list, context: ExecutionContext) -> list[list]:

        id, feature_atoms = arguments

        features = {atom.arguments[1]: atom.arguments[2] for atom in feature_atoms}

        ok = check_pronoun(id, features, self.entities)

        print(id, features, ok)

        if ok:
            return [[None, None]]
        else:
            return []

    # ('update_saliency', atoms)
    def update_saliency(self, arguments: list, context: ExecutionContext) -> list[list]:

        decay_saliency(self.entities)

        process_atoms(arguments[0], self.entities)

        update_features(self.entities, context.solver)

        return [[None]]
