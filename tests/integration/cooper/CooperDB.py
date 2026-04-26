import sqlite3
from vrel.data_source.Sqlite3DataSource import Sqlite3DataSource


class CooperDB(Sqlite3DataSource):
    # Using an in-memory sqlite database to store the facts
    def __init__(self):

        connection = sqlite3.connect(":memory:")
        cursor = connection.cursor()

        # note: same entity may have multiple names
        cursor.execute("CREATE TABLE entity (id INTEGER PRIMARY KEY, name TEXT)")

        cursor.execute("CREATE TABLE metal (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE metallic (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE element (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE compound (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE solid (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE gas (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE nonmetal (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE white (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE dark_gray (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE brittle (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE oxide (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE sulfide (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE chloride (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE fuel (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE burns (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE burns_rapidly (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE combustable (id INTEGER PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE gasoline (id INTEGER PRIMARY KEY, truth TEXT)")

        super().__init__(connection)
