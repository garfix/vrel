from abc import ABC, abstractmethod

from vrel.entity.Id import Id
from vrel.entity.Relation import Relation


class SomeDataSource(ABC):
    """
    Implement this interface to give the library access to any type of data source be it an SQL database, NoSQL database, in-memory array or even CSV file.
    """

    @abstractmethod
    def select(self, relation: Relation, columns: list[str], values: list) -> list[list]:
        """
        This method treats datasource access as were it a simple SQL SELECT statement:
        SELECT <columns>+ FROM <table> WHERE <column>=<value>*
        One or more columns (column1, column1, ...), zero or more where clauses (columns1=values1 AND columns1=values1, ...)
        Note that same columns are both used in the "select" and the "where"
        Note that if a value is None, it must be omitted from the "where"
        """
        raise Exception("select not implemented")

    def select_column(self, relation: Relation, columns: list[str], values: list) -> list:
        return [row[0] for row in self.select(relation, columns, values)]

    def insert(self, relation: Relation, columns: list[str], values: list):
        raise Exception("insert not implemented")

    def clear(self):
        raise Exception("clear not implemented")

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
