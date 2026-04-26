from itertools import product

from vrel.core.constants import E1, E2
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Relation import Relation
from vrel.interface.SomeModel import SomeModel


class SameAs:
    model: SomeModel

    def __init__(self, model: SomeModel) -> None:
        self.model = model

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

    def get_same_as(self, id: int) -> list[int]:

        relations = self.model.find_relations("same_as")
        if len(relations) == 0:
            return [id]

        relation = relations[0]
        context = ExecutionContext(relation, self, None, self.model)
        results = relation.query_function([E1, E2], context)
        variants = set([id])
        for result in results:
            if result[0] == str(id):
                variants.add(int(result[1]))
            elif result[1] == str(id):
                variants.add(int(result[0]))
        # print(id)
        # print(results)
        # print(variants)
        return list(variants)
