from itertools import product
import json

from vrel.core.Logger import Logger
from vrel.core.constants import E1, E2, SAME_AS
from vrel.entity.ExecutionContext import ExecutionContext
from vrel.entity.Id import Id
from vrel.entity.Relation import Parameter, Relation
from vrel.entity.Variable import Variable
from vrel.interface.SomeModel import SomeModel
from vrel.interface.SomeSameAsHandler import SomeSameAsHandler
from vrel.module.SqliteMemoryModule import SqliteMemoryModule


class SameAsModule(SomeSameAsHandler, SqliteMemoryModule):

    model: SomeModel
    id_variants: dict

    def __init__(self) -> None:
        super().__init__()

        self.id_variants = None

        self.add_relation(
            Relation(
                SAME_AS,
                parameters=[Parameter("id1", None), Parameter("id2", None)],
                query_function=self.same_as_read,
                write_function=self.same_as_write,
            )
        )

    def same_as_read(self, arguments: list, context: ExecutionContext) -> list[list]:
        term1, term2 = arguments

        if isinstance(term1, Variable) and isinstance(term2, Variable):
            same_as = self.get_relation(SAME_AS)
            results = self.select(same_as, ["id1", "id2"], [term1, term2])

            hydrated = []
            for result in results:
                row = []
                for e in result:
                    data = json.loads(e)
                    row.append(Id(data["id"], data["type"]))
                hydrated.append(row)

            return hydrated

        handler = context.model.get_same_as_handler()
        if handler and handler.same_as(term1, term2):
            return [[None, None]]
        else:
            return []

    def same_as_write(self, arguments: list, context: ExecutionContext) -> list[list]:

        dehydrated = [json.dumps({"id": id.id, "type": id.type}) for id in arguments]
        return self.write(dehydrated, context)

    def get_same_as_variants(self, bound_arguments: list, relation: Relation):

        group = []
        for i, formal in enumerate(relation.parameters):
            if isinstance(bound_arguments[i], Id):
                group.append(self.get_same_as(bound_arguments[i]))
            else:
                group.append([bound_arguments[i]])

        # Carthesian product to produce all combinations that the lists in group allow
        result = [list(t) for t in product(*group)]

        return result

    def clear_cache(self):
        self.id_variants = None

    def get_same_as(self, id: Id) -> list[int | str]:
        if self.id_variants is None:
            self.build_cache()

        if id.type in self.id_variants and str(id.id) in self.id_variants[id.type]:
            return self.id_variants[id.type][str(id.id)]
        else:
            return [id]

    def same_as(self, id1: Id, id2: Id):
        return id2 in self.get_same_as(id1)

    def build_cache(self):
        relations = self.model.find_relations(SAME_AS)
        if len(relations) == 0:
            return [id]

        self.id_variants = {}

        relation = relations[0]
        context = ExecutionContext(relation, None, None, self.model, Logger())
        results = relation.query_function([E1, E2], context)

        for result in results:
            id1, id2 = result
            if not id1.type in self.id_variants:
                self.id_variants[id1.type] = {}
            if not id2.type in self.id_variants:
                self.id_variants[id2.type] = {}

            if str(id1.id) not in self.id_variants[id1.type]:
                self.id_variants[id1.type][str(id1.id)] = [id1]
            if str(id2.id) not in self.id_variants[id2.type]:
                self.id_variants[id2.type][str(id2.id)] = [id2]
            self.id_variants[id1.type][str(id1.id)].append(id2)
            self.id_variants[id2.type][str(id2.id)].append(id1)

    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE same_as (entity_type TEXT, id1 TEXT, id2 TEXT)")


class DummySameAsHandler(SomeSameAsHandler):
    def get_same_as_variants(self, bound_arguments: list, relation: Relation) -> list[list]:
        return [bound_arguments]

    def clear_cache(self):
        return
