# Getting started

To appreciate how the library works, best have a look at one of the demo `test.py` files.

On this page I'll show you the process of creating a single sentence to access a database.

In this example we'll query the table `employee` from our database and ask it "Who is the oldest employee?"

## A data source

Perhaps you have a database and you can use it as a data source. Otherwise we'll create a SQLite database, create a table `employee` and here and populate it with some data:

```python
connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
cursor.execute("CREATE TABLE employee (id INT PRIMARY KEY, name TEXT, birth_date DATE)")
cursor.execute("INSERT INTO employee (id, name, birth_date) VALUES (1, 'Patrick', '1969-11-24')")
cursor.execute("INSERT INTO employee (id, name, birth_date) VALUES (2, 'Jackie', '1984-02-12')")
cursor.execute("INSERT INTO employee (id, name, birth_date) VALUES (3, 'Barbara', '1962-07-30')")
cursor.execute("INSERT INTO employee (id, name, birth_date) VALUES (4, 'Billy', '2003-01-15')")
```

In both cases we'll need to wrap the connection with a data source:

```python
db = Sqlite3DataSource(connection)
```

## A module

Based on this data source we'll now create relations. For this, we need to create a module.

```python
class StartModule(SomeModule):

    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()

        self.data_source = data_source

        self.add_relation(
            Relation(
                "employee",
                query_function=self.simple_entity,
                parameters=[
                    Parameter("id", "person"),
                    Parameter("name", str),
                    Parameter("birth_date", date),
                ],
            )
        )

        self.add_relation(
            Relation(
                "age",
                query_function=self.age,
                parameters=[
                    Parameter("id", "person"),
                    Parameter("age", float),
                ],
            )
        )

    def simple_entity(self, arguments: list, context: ExecutionContext) -> list[list]:
        return self.select(context.relation, ["id"], arguments)

    def age(self, arguments: list, context: ExecutionContext) -> list[list]:
        results = self.select(self.get_relation("employee"), ["id", "birth_date"], arguments)

        ages = [[result[0], calculate_age(result[1])] for result in results]
        return ages


def calculate_age(birth_date: str) -> int:
    birth = date.fromisoformat(birth_date)  # parses "yyyy-mm-dd"
    today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
```

This module creates 2 relations: `employee` and `age`. Each relation has parameters and a query function. Note that the `age` function calculates the age from the birth date of the employee.

Let's instanciate the module

```python
facts = StartModule(db)
```

## The read grammar

To parse the sentence, the parser needs grammar rules. Let's specify create a file called `read_grammar.py` and function `get_read_grammar`.

```python
def get_read_grammar():
    return [
        # sentence
        {
            # Example: Who is the oldest employee?
            "syn": "s(E1) -> 'who' 'is' np(E1) + '?'",
            "sem": lambda np: Atom("intent_single_name", [np]),
        },
        {
            # Bye
            "syn": "s(E1) -> 'bye'",
            "sem": lambda: Atom(
                "intent_close_conversation",
            ),
        },
        # np
        {
            "syn": "np(E1) -> aggregate(E1)",
            "sem": lambda aggregate: aggregate,
        },
        # aggregates
        {
            "syn": "aggregate(E1) -> 'the' 'oldest' nbar(E1)",
            "sem": lambda nbar: Atom("arg_max", E1, Age, [nbar], [Atom("age", E1, Age)]),
        },
        # nbar
        {
            "syn": "nbar(E1) -> noun(E1)",
            "sem": lambda noun: noun,
        },
        # noun
        {"syn": "noun(E1) -> 'employee'", "sem": lambda: Atom("employee", E1)},
    ]

```

The grammar has two sentece-level rules (whose head is `s()`). Both create an **intent** atom. The intent is the function that knows what to do with this kind of sentence. Our sample sentence matches the first sentence rule, which contains the clause `np(E1)` that stands for any noun phrase. The `np` is **rewritten** by the rule whose head is `np(E1)`. The `np` rewrites to an aggregate, and the aggregate rewrites to "the oldest" `nbar`. An nbar is a noun phrase without a determiner, and it rewrites to a `noun`. The only noun in this grammar is "employee". The semantics of the noun is the atom `Atom("employee", E1)`.

Note that each rule has both a syntactic component ("syn") and a semantic attachment ("sem"). The latter contains a piece of the executable meaning of the sentence.

From this grammar the parser is able to construct the parse tree

```

TODO

```

and the semantic composer combines the semantic attachments of this sentence to the representation

```
TODO
```

## Last words

All code in this page can be found in the directory `tests/start`.
