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

## The model

A **model** represents a domain of knowledge. In this library the model is simply a container for all modules.

## The parser

The basic function of a **parser** is to turn a sentence (string of characters) into a syntax tree. We're using **Earley's algorithm** here. It produces not one tree, but a "forest" of **syntactically ambiguous** trees.

The parser uses heuristics to rank the trees in decreasing fitness. The best tree is then used first.

Th parser is also able to extract multiple (unambiguous) sentences from a single paragraph. The sentences do not need to be handled in separately. And it uses individual characters as tokens, rather than words, in order to serve as a morphological parser and syntactic parser in one.

## The semantic composer

The **semantic composer** creates a logical structure by combining the semantic attachments of the syntax tree.

## The executor

The **executor** just **executes** the logical structure.

## The system

The **system** of the library brings together a model, and some "processors": a parser, a semantic composer and an executor. Each of these has a standard class, but each of these may be overridden, or even replaced by another, if you like. When the system is complete, one can ask it to process a sentence.

## The solver

The **solver** is not a component you would interact with directly, but it's useful to know about it's central function. The solver takes a list of unbound atoms as input and returns a list of variable bindings.
