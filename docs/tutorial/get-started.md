# Getting started

On this page I'll guide you through the process of accessing a database through natural language with Vrel.

In this example we'll query the table `employee`, with columns `id`, `name`, and `birth_date`, from our database and ask it "Who is the oldest employee?"

Note: all code in this page can be found in the directory `tests/start`.

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
            "sem": lambda np: Atom("intent_list", [np]),
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

The grammar has two sentence-level rules (whose head is `s()`). Both create an **intent** atom. An intent is a function that implements what to do with this kind of sentence. Our sample sentence matches the first sentence rule, which contains the clause `np(E1)` that stands for any noun phrase. The `np` is **rewritten** by the rule whose head is `np(E1)`. The `np` rewrites to an aggregate, and the aggregate rewrites to "the oldest" `nbar`. An nbar is a noun phrase without a determiner, and it rewrites to a `noun`. The only noun in this grammar is "employee". The semantics of the noun is the atom `Atom("employee", E1)`.

Note that each rule has both a syntactic component ("syn") and a semantic attachment ("sem"). The latter contains a piece of the executable meaning of the sentence.

Create the parser and add these rules

```python
parser = BasicParser()
parser.add_grammar_rules(get_read_grammar())
```

From this grammar the parser is able to construct the parse tree

```
s
+- who 'who'
+-   ' '
+- is 'is'
+-   ' '
+- np
|  +- aggregate
|     +- the 'the'
|     +-   ' '
|     +- oldest 'oldest'
|     +-   ' '
|     +- nbar
|        +- noun
|           +- employee 'employee'
+- ? '?'
```

and the semantic composer combines the semantic attachments of this sentence to the representation

```
 (intent_list
    1. [
         (arg_max
            1. $1
            2. $2
            3. [
                 (employee
                    1. $1)
            ]
            4. [
                 (age
                    1. $1
                    2. $2)
            ])
    ])

```

## Intents

Once the executable meaning of a sentence is known, execution can begin. The top-level of a sentence's meaning if formed by its **intent**. This intent determines what to do with the sentence. Commands are treated different than questions, and one question is treated differently from another. At the same time, multiple semantic structures can be handled by the same intent. The intent can be seen as the envelope of the semantics, and is implemented in Prolog-syntax. Here's one

```
intent_list(E1, Sem) :-
    find_all(E1, Sem, Elements),
    out('list', Elements).
```

The head of this rule matches the top-level semantics of our sentence, therefore the body is executed. The body finds all values of `E1` and places them in a list called `Elements`. This list is then stored for output.

The intents are stored in a file called `intents.pl` and loaded like this

```python
inferences = DeductionModule()
inferences.import_rules(path / "intents.pl")
```

## The model

All modules are combined in the model.

```python
model = Model([facts, inferences])
```

## Generation

The answer, in the form of a semantic structure (`out('list', Elements)`), needs to be converted into a sentence. This is the work of the generator. The generator is rule-based like the parser and reads its rules like this:

```python
generator = BasicGenerator(model)
generator.add_grammar_rules(get_en_us_write_grammar())
generator.add_grammar_rules(get_write_grammar())
```

The rules themselves look like this:

```python
# sentence
{
    "syn": "s() -> np(E1)",
    "if": [Atom("last_output", "list", E1)],
    "list_element": E1,
    "list_combine": lambda nps: ", ".join(nps),
},

# noun phrases
{
    "syn": "np(E1) -> literal(Name)",
    "if": [Atom("name", E1, Name)]
},
```

The generator starts the new sentence with the category `s()`. It then tries to find a rule to match this category, based on the head of the rule and the `if` condition. It then replaces the `s()` by the body categories; here: `np(E1)`. Next, a rule for the `np(E1)` is found and `np(E1)` is rewritten by `Name`, the name of the element `E1` used as-is. The result is the (literal) value `Barbara`.

The question itself allows only a single answer, but as the solver creates lists of answers, answers are treated as lists here.

The `list_element` and `list_combine` constructs take the list `E1` apart and handle its elements one by one. Each element is rewritten separately, and the results are combined using `list_combine`. In this case there's just one element.

## The system

The system combines the objects we have built:

```python
system = BasicSystem(
    model=model,
    parser=parser,
    composer=composer,
    executor=executor,
    output_generator=generator,
)
```

## Asking the question

Once the system is set up, we can use it to ask a question

```python
system.enter(SentenceRequest("Who is the oldest employee?"))
output = generator.generate_output()
```

`output` gives us the answer ("Barbara")

## Automates tests

To continue working on the system, add another request and response to the test suite and run

```python
tester = DialogTester(self, tests, system)
tester.run()
```

The tester enters all sentences automatically and checks if the answer of the library is still right.
