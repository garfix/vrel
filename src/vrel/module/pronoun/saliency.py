from vrel.core.constants import E1, FEATURE, SEM_FUNCTION_INDIRECT_OBJECT, SEM_FUNCTION_OBJECT, SEM_FUNCTION_SUBJECT
from vrel.entity.Atom import Atom
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Id import Id

from dataclasses import dataclass

from vrel.entity.Variable import Variable
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeSolver import SomeSolver

DECAY = 0.5
THRESHOLD = 0.125


@dataclass(frozen=False)
class EntityData:
    ids: list[Id]
    saliency: int
    features: dict[str, str]


# 0 = subject, 1 = object, 2 = indirect object
score = {SEM_FUNCTION_SUBJECT: 3, SEM_FUNCTION_OBJECT: 2, SEM_FUNCTION_INDIRECT_OBJECT: 1}


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
        entities.append(EntityData([id], saliency, {}))
    else:
        entities[index].saliency += saliency


def consolidate_entities(entities: list[EntityData], context: ExecutionContext):
    """
    Merges entities whose ids are same_as.
    """

    # print("e1", entities)

    # complete ids with all known variants
    for entity in entities:
        entity.ids = context.model.get_same_as_handler().get_same_as(entity.ids[0])

    # print("e2", entities)

    # merge entities
    new_entities = []
    for entity in entities:
        found: EntityData | False = False
        for e in new_entities:
            if entity.ids[0] in e.ids:
                found = e
                break

        if found != False:
            found.features = found.features | entity.features
            found.saliency = max(found.saliency, entity.saliency)
        else:
            new_entities.append(entity)

    # print("e3", new_entities)

    return new_entities


def decay_saliency(entities: list[EntityData]):
    for entity in entities:
        entity.saliency *= DECAY


def update_features(entities: list[EntityData], solver: SomeSolver):
    for entity in entities:
        bindings = solver.solve([Atom(FEATURE, entity.ids[0], Variable("Name"), Variable("Value"))])
        for binding in bindings:
            print("BINDING", binding)
            entity.features[binding["Name"]] = binding["Value"]


def find_index(id: Id, entities: list[EntityData]):
    index = None
    for i, entity in enumerate(entities):
        for entity_id in entity.ids:
            if entity_id == id:
                index = i
                break
    return index


def find_entity(id: Id, entities: list[EntityData]):
    for entity in entities:
        for entity_id in entity.ids:
            if entity_id == id:
                return entity
    return None


def find_matching_entity(id: Id, features: dict[str, str], entities: list[EntityData]) -> EntityData | None:
    entity = find_entity(id, entities)
    if not entity:
        return None

    # sort entities by decreasing saliency
    sorted_entities = sorted(entities, key=lambda entity: entity.saliency, reverse=True)

    matching_entities = get_salient_entities(features, sorted_entities)
    return matching_entities[0] if len(matching_entities) > 0 else None


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
            salient_entities.append(entity)

    return salient_entities


def check_pronoun(id: Id, features: list[Atom], entities: list[EntityData]):

    # print("id", id)
    # print("features", features)
    # print("entities", entities)

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
    found = False
    for salient_entity in salient_entities:
        if id in salient_entity.ids:
            found = True
    if not found:
        return False

    print("3", salient_entities)

    # the pronoun would be ambiguous: don't use the pronoun
    if len(salient_entities) > 1:
        return False

    print("4")

    return True
