import sqlite3
from vrel.data_source.Sqlite3DataSource import Sqlite3DataSource


class SimpleDB(Sqlite3DataSource):
    # Using an in-memory sqlite database to store the facts
    def __init__(self):

        connection = sqlite3.connect(":memory:")
        cursor = connection.cursor()

        # note: same entity may have multiple names
        cursor.execute("CREATE TABLE entity (id INTEGER PRIMARY KEY, name TEXT)")

        super().__init__(connection)
