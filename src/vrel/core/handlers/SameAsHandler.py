from itertools import product

from vrel.core.Logger import Logger
from vrel.core.constants import E1, E2, SAME_AS
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Relation import Relation
from vrel.entity.Variable import Variable
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeSameAsHandler import SomeSameAsHandler

ET = Variable("ET")


class SameAsHandler(SomeSameAsHandler):
    """
    This plugin implements the query part of the same_as relation.
    The same_as relation declares that some id1 should be treated the same as some id2 everywhere in the database.
    This handler does that by creating alternatives for queries.
    If a query is `parent(13, E1)` and id 13 is the same as id 20 and 44 in the database, it returns
    * parent(13, E1)
    * parent(20, E1)
    * parent(44, E1)
    The solver then executes all three queries.
    """

    model: SomeModel
    id_variants: dict

    def __init__(self) -> None:
        self.id_variants = None

    def get_same_as_variants(self, bound_arguments: list, relation: Relation):
        if relation.parameters is None:
            return [bound_arguments]

        group = []
        for i, formal in enumerate(relation.parameters):
            # todo: generalize
            if formal.entity_type is not None:
                # if formal == "id" or relation.predicate == "pick_up":
                # if not isinstance(bound_arguments[i], list):
                group.append(self.get_same_as(formal.entity_type, bound_arguments[i]))
            else:
                group.append([bound_arguments[i]])

        # Carthesian product to produce all combinations that the lists in group allow
        result = list(product(*group))

        return result

    def clear_cache(self):
        self.id_variants = None

    def get_same_as(self, entity_type: str, id: int | str) -> list[int | str]:
        if self.id_variants is None:
            self.build_cache()

        if entity_type in self.id_variants and str(id) in self.id_variants[entity_type]:
            return self.id_variants[entity_type][str(id)]
        else:
            return [id]

    def same_as(self, entity_type: str, id1: int | str, id2: int | str):
        return str(id2) in self.get_same_as(entity_type, str(id1))

    def build_cache(self):
        relations = self.model.find_relations(SAME_AS)
        if len(relations) == 0:
            return [id]

        self.id_variants = {}

        relation = relations[0]
        context = ExecutionContext(relation, None, None, self.model, Logger())
        results = relation.query_function([ET, E1, E2], context)

        for result in results:
            entity_type, id1, id2 = result
            if not entity_type in self.id_variants:
                self.id_variants[entity_type] = {}
            if id1 not in self.id_variants[entity_type]:
                self.id_variants[entity_type][id1] = [id1]
            if id2 not in self.id_variants[entity_type]:
                self.id_variants[entity_type][id2] = [id2]
            self.id_variants[entity_type][id1].append(id2)
            self.id_variants[entity_type][id2].append(id1)
