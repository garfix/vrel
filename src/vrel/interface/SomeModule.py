from abc import ABC, abstractmethod

from vrel.entity.Id import Id
from vrel.entity.Relation import Relation
from vrel.interface.SomeDataSource import SomeDataSource


class SomeModule(ABC):

    relations: dict
    data_source: SomeDataSource

    def __init__(self) -> None:
        self.relations = {}

    def add_relation(self, relation: Relation):
        self.relations[relation.predicate] = relation

    def get_relation(self, predicate: str) -> Relation | None:
        return self.relations[predicate] if predicate in self.relations else None

    def select(self, relation: Relation, columns: list[str], values: list[str]):
        values = self.data_source.select(relation.predicate, columns, values)
        return [self.hydrate(relation, columns, row) for row in values]

    def select_column(self, relation: Relation, columns: list[str], values: list[str]):
        values = self.select(relation, columns, values)
        return [row[0] for row in values]

    def insert(self, relation: Relation, columns: list[str], values: list[str]):
        self.data_source.insert(relation.predicate, columns, values)

    def delete(self, relation: Relation, columns: list[str], values: list):
        self.data_source.delete(relation.predicate, columns, values)

    def hydrate(self, relation: Relation, columns: list[str], values: list):
        if relation.parameters is None:
            raise Exception(f"{relation.predicate} has no parameters")

        new_values = []
        for value, column in zip(values, columns):
            parameter = relation.get_parameter_by_name(column)
            if not parameter:
                raise Exception(f"Parameter not found in relation {relation.predicate}: {column}")
            if isinstance(parameter.type, str):
                new_value = Id(value, parameter.type)
            else:
                new_value = value
            new_values.append(new_value)

        return new_values
