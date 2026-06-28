## Data source

A **data source** is a class that wraps any database via standardized methods:

- `select(self, table: str, columns: list[str], values: list)`
- `insert(self, table: str, columns: list[str], values: list)`
- `delete(self, table: str, columns: list[str], values: list)`
- `clear(self)`

The analogy to SQL will be clear. **select** `SELECT`s all tuples of table `WHERE` column = value (for each column/value pair). **delete** and **insert** are similar. Implement **clear** only if you are comfortable with deleting all tuples from the data source.

Data sources are available for common databases like MySQL, SQLite, PostgreSQL and Sparql. It is relatively easy to add your own data source. The source may be something other than a database as well, but it should result in tuples.

## Module

A **module** is a class that implements the meaning / function of some relations. Creating a module for your application is a common thing to do. A relation can be implemented by selecting and inserting into a data source, but many relations are implemented by a custom function as well.

There are several standard modules that provide a variety of functionalities:

- The **CoreModule** (which is always included) provides relations (functions) like `less_than`, `greater_than`, `sum`, `avg`, `not`, etc
- The **OptimizerModule** provides functions that are needed to efficiently perform complex queries
- The **DeductionModule** lets you include deduction rules in a (stripped-down) Prolog format.
- The **InductionModule** lets you include induction rules to build goal chains
- The **GrammarModule** lets you create new grammar rules in a dialog (a rare thing to do)
- The **SameAsModule** lets you treat different id's as the same in queries
- The **PronounModule** lets you keep track of the saliency of entities, as needed by pronoun resolution
