# Data sources

By **data sources** we mean databases and other sources of data. A data source provides access to any kind of tabular data. The library has standard data sources for PostgreSQL (via PsycoPg2 and PsycoPg3), MySQL, Sqlite3, Sparql, and its simple built-in in-memory db MemoryDB.

A data source is used by a model to retrieve and store rows of data.

## PostgreSQL (PsycoPg2)

This code shows how to create data source based on a Postgres database, accessed via PsycoPg2. PsycoPg2 can be installed with `pip install psycopg2-binary`.

```python
from richard.data_source.PsycoPg2DataSource import PsycoPg2DataSource
import psycopg2

connection = psycopg2.connect(
    database='my_database', # Your database
    host='127.0.0.1',
    user='patrick', # Your username
    password='test123', # Your password
    port=5432
)

ds = PsycoPg2DataSource(connection)
```

## Postgres (PsychoPg3)

This code shows how to create data source based on a Postgres database, accessed via PsycoPg3. PsycoPg3 can be installed with `pip install "psycopg[binary]"`.

```python
from richard.data_source.PsycoPg3DataSource import PsycoPg3DataSource
import psycopg

with psycopg.connect(
    dbname='my_database', # Your database
    host='127.0.0.1',
    user='patrick', # Your username
    password='test123', # Your password
    port=5432
) as connection:

ds = PsycoPg3DataSource(connection)
```

## MySQL

This code shows how to create data source based on a MySQL database. The MySQL connector can be installed with `pip install mysql-connector-python"`.

```python
from richard.data_source.MySqlDataSource import MySqlDataSource
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="patrick",  # Your username
    password="test123",  # Your password
    database="my_database"  # Your database name
)

ds = MySqlDataSource(connection)
```

## SQLite3

This code shows how to create data source based on a SQLite3 database.

```python
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource

connection = sqlite3.connect(':memory:')
ds = Sqlite3DataSource(connection)
```

## SPARQL

There's a basic adapter for SPARQL databases, that will likely need to be extended for practical use.

Here's example code that creates a custom class (here: WikidataDataSource) that wraps `SparqlDataSource` with custom configuration. The reason for this approach is that each of the methods of the base class can be overridden as needed.

```python
class WikidataDataSource(SparqlDataSource):

    def __init__(self, result_cache_path: bool=None):
        """
        It's important to add a proper User Agent or you will get many 403 denied responses
        If you intend to use this data source for your own application, change it to something personal

        see also: https://foundation.wikimedia.org/wiki/Policy:User-Agent_policy
        """
        super().__init__("https://query.wikidata.org/sparql",
            result_cache_path=result_cache_path,
            headers={
                "User-Agent": "YOUR_REPO_NAME/1.0 (https://github.com/PATH_TO_YOUR_REPO; YOUR_EMAIL_ADDRESS) YOUR_REPO_NAME/VERSION"
            }
        )
```

The `result_cache_path` is the name of a directory where you can cache SPARQL results. Caching will cause a big performance gain for recurring queries.

## Create a custom data source

Data sources for other relational databases can be added easily. Other services can be added as data source as well. And this will be described here.

Any data source takes the shape of an adapter that makes the underlaying data available via this standard signature:

```python
def select(self, table: str, columns: list[str], values: list[Simple]) -> list[list[Simple]]:
```

Compare this signature to an SQL select query:

```sql
SELECT `columns` FROM `table` WHERE `column1`=`value1` AND `column2` = `value2`;
```

Note that same columns are both used in the "select" and the "where" clauses.
Note that if a value is `None`, it must be omitted from the "where" clause.

To add a new data source, copy an existing one that best looks like the one you need, and make changes to it. To give you an idea, here's the implementation of `PsycoPg2DataSource`:

```python
def select(self, table: str, columns: list[str], values: list[Simple]) -> list[list[Simple]]:

    import psycopg2

    where = "TRUE"
    variables = []
    for column, value in zip(columns, values):
        if value is not None:
            where += f" AND {column}=%s"
            variables.append(value)

    cursor = self.connection.cursor(cursor_factory=psycopg2.extensions.cursor)
    select = ','.join(columns)
    cursor.execute(f"SELECT {select} FROM {table} WHERE {where}", variables)
    return [list(row) for row in (cursor.fetchall())]
```

If the data source is able to write as well as read, it implements this signature:

```python
def insert(self, table: str, columns: list[str], values: list):
```

Compare this signature to an SQL insert query:

```sql
INSERT INTO `table` (`column1`, `column2`) VALUES (`value1`, `value2`);
```
