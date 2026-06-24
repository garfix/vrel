from vrel.core.constants import E1, FEATURE
from vrel.entity.Atom import Atom
from vrel.entity.Id import Id

from dataclasses import dataclass

from vrel.entity.Variable import Variable
from vrel.interface.SomeSolver import SomeSolver

DECAY = 0.5
THRESHOLD = 0.125


@dataclass(frozen=True)
class EntityData:
    id: Id
    saliency: int
    features: dict[str, str]


# 0 = subject, 1 = object, 2 = indirect object
score = {0: 3, 1: 2, 2: 1}


def process_atoms(atoms: list[Atom], entities: list[EntityData]):
    for atom in atoms:
        i = 0
        for argument in atom.arguments:
            if i == 0 and isinstance(argument, Id) and argument.type == "event":
                i = i - 1
            else:
                if isinstance(argument, Id):
                    update_saliency(argument, score[i], entities)
            i += 1


def update_saliency(id: Id, saliency: int, entities: list[EntityData]):
    index = find_index(id, entities)
    if index == None:
        entities.append(EntityData(id, saliency, {}))
    else:
        entities[index].saliency += saliency


def decay_saliency(entities: list[EntityData]):
    for entity in entities:
        entity.saliency *= DECAY


def update_features(entities: list[EntityData], solver: SomeSolver):
    for entity in entities:
        bindings = solver.solve([Atom(FEATURE, entity.id, Variable("Name"), Variable("Value"))])
        print(entity.id, bindings)
        for binding in bindings:
            entity.features[binding["Name"]] = binding["Value"]


def find_index(id: Id, entities: list[EntityData]):
    index = None
    for i, entity in enumerate(entities):
        if entity.id == id:
            index = i
            break
    return index


def get_salient_entities(features: dict[str, str], entities: list[EntityData]) -> list[Id]:
    salient_entities = []

    for entity in entities:
        if entity.saliency < THRESHOLD:
            continue
        ok = True
        for name, value in features.items():
            if name not in entity.features or entity.features[name] != value:
                ok = False

        if ok:
            salient_entities.append(entity.id)

    return salient_entities


def check_pronoun(id: Id, features: list[Atom], entities: list[EntityData]):

    index = find_index(id, entities)
    if index == None:
        return False

    data = entities[index]

    # entity too old: don't use a pronoun
    saliency = data.saliency
    if saliency < THRESHOLD:
        return False

    salient_entities = get_salient_entities(features, entities)

    # entity does not match features: don't use its pronoun
    if id not in salient_entities:
        return False

    # the pronoun would be ambiguous: don't use the pronoun
    if len(salient_entities) > 1:
        return False

    return True
