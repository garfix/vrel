from itertools import product

from vrel.core.constants import E1, E2, SAME_AS
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Relation import Relation
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeSameAsHandler import SomeSameAsHandler


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

    def __init__(self, model: SomeModel) -> None:
        self.model = model
        self.id_variants = None

    def get_same_as_variants(self, bound_arguments: list, relation: Relation):
        if relation.formal_parameters is None:
            return [bound_arguments]

        group = []
        for i, formal in enumerate(relation.formal_parameters):
            # todo: generalize
            if formal == "id":
                group.append(self.get_same_as(bound_arguments[i]))
            else:
                group.append([bound_arguments[i]])

        # Carthesian product to produce all combinations that the lists in group allow
        result = list(product(*group))

        return result

    def clear_cache(self):
        self.id_variants = None

    def get_same_as(self, id: int) -> list[int]:
        if self.id_variants is None:
            self.build_cache()

        if id in self.id_variants:
            return self.id_variants[id]
        else:
            return [id]

    def build_cache(self):
        relations = self.model.find_relations(SAME_AS)
        if len(relations) == 0:
            return [id]

        self.id_variants = {}

        relation = relations[0]
        context = ExecutionContext(relation, None, None, self.model)
        results = relation.query_function([E1, E2], context)

        for result in results:
            id1, id2 = result
            if id1 not in self.id_variants:
                self.id_variants[int(id1)] = [int(id1)]
            if id2 not in self.id_variants:
                self.id_variants[int(id2)] = [int(id2)]
            self.id_variants[int(id1)].append(int(id2))
            self.id_variants[int(id2)].append(int(id1))
