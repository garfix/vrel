from vrel.core.constants import AUTO
from vrel.entity.Id import Id
from vrel.entity.Relation import Relation
from vrel.entity.Variable import Variable
from vrel.interface.SomeDataSource import SomeDataSource


class Sqlite3DataSource(SomeDataSource):

    connection: any

    def __init__(self, connection):
        self.connection = connection

    def select(self, relation: Relation, values: list) -> list[list]:

        table = relation.predicate
        columns = relation.get_parameter_names()

        where = "TRUE"
        variables = []
        for column, term in zip(columns, values):
            if isinstance(term, Id):
                where += f" AND {column}=?"
                variables.append(term.id)
            elif not isinstance(term, Variable):
                where += f" AND {column}=?"
                variables.append(term)

        cursor = self.connection.cursor()
        select = ",".join(columns)
        cursor.execute(f"SELECT {select} FROM {table} WHERE {where}", variables)
        return [self.hydrate(relation, list(row)) for row in (cursor.fetchall())]

    def insert(self, relation: Relation, values: list):

        table = relation.predicate
        columns = relation.get_parameter_names()

        cursor = self.connection.cursor()
        column_string = ",".join(columns)
        place_holders = ", ".join(["?" for v in values])
        # values = [None if v == AUTO else v for v in values]

        sql_values = []
        for v in values:
            if v == AUTO:
                sql_values.append(None)
            elif isinstance(v, Id):
                sql_values.append(v.id)
            else:
                sql_values.append(v)

        cursor.execute(f"INSERT OR IGNORE INTO {table} ({column_string}) VALUES ({place_holders})", sql_values)

    def delete(self, relation: Relation, values: list):

        table = relation.predicate
        columns = relation.get_parameter_names()

        cursor = self.connection.cursor()
        place_holders = "AND ".join([f"{c} = ? " for c in columns])
        cursor.execute(f"DELETE FROM {table} WHERE {place_holders}", values)

    def clear(self):
        raise Exception("clear not implemented")
