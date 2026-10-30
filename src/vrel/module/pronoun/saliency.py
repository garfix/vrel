from vrel.core.constants import E1, FEATURE, FUNCTION_INDIRECT_OBJECT, FUNCTION_OBJECT, FUNCTION_SUBJECT
from vrel.entity.Atom import Atom
from vrel.entity.Id import Id

from dataclasses import dataclass

from vrel.entity.Variable import Variable
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeSolver import SomeSolver

DECAY = 0.5
THRESHOLD = 0.125


@dataclass(frozen=False)
class EntityData:
    id: Id
    saliency: int
    features: dict[str, str]


# 0 = subject, 1 = object, 2 = indirect object
score = {FUNCTION_SUBJECT: 3, FUNCTION_OBJECT: 2, FUNCTION_INDIRECT_OBJECT: 1}


def process_atoms(atoms: list[Atom], entities: list[EntityData], model: SomeModel):
    print("process", atoms)
    for atom in atoms:

        relations = model.find_relations(atom.predicate)
        for relation in relations:
            for i, argument in enumerate(atom.arguments):
                parameter = relation.parameters[i]
                f = parameter.function
                if f:
                    if isinstance(argument, Id):
                        update_saliency(argument, score[f], entities)
                    else:
                        print("what about", argument)


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

    print("id", id)
    print("features", features)
    print("entities", entities)

    index = find_index(id, entities)
    if index == None:
        return False

    print("1")

    data = entities[index]

    # entity too old: don't use a pronoun
    saliency = data.saliency
    if saliency < THRESHOLD:
        return False

    print("2")

    salient_entities = get_salient_entities(features, entities)

    # entity does not match features: don't use its pronoun
    if id not in salient_entities:
        return False

    print("3", salient_entities)

    # the pronoun would be ambiguous: don't use the pronoun
    if len(salient_entities) > 1:
        return False

    print("4")

    return True
