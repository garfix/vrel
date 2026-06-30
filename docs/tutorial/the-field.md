You need to understand some concepts in the field in order to use the library.

## Logic and semantics

A natural language processor such as this turns a sentence into a semantic representation. What do we mean by that? In this library We mean that it's an **executable logical representation** whose entities and relations are **meaningful concepts to the user**.

Reasoning in this library follows the rules of **Prolog** for deduction, which is by itself based on predicate logic and Horn clauses.

## Entities and relations

The common name for anything that can be instantiated is an **entity**. A `person`, `dog`, `employment`, `birthday`, etc. A **relation** is a meaningful, named group of entities: `owns`, `parent`, `caused_by`. "meaningful" here means that it has some function in the application.

A relation is named by its **predicate** (`person`, `owns`, etc) and its **(formal) parameters**. An instance of a relation is a **tuple** and the instances of parameters are called **arguments**.

| abstract  | concrete |
| --------- | -------- |
| entity    | instance |
| relation  | tuple    |
| parameter | argument |

## Relations

A relation, with its predicate and parameters is the building block of both logic and programming. It can be a piece of data, or it can be a function. In this library, the relation has a **query** function and a **write** function.

The query function uses the relation as a filter, similar to SQL's `SELECT`. The output is a series of tuples that match the arguments. This is natural for database access, but less intuitive for custom functions. A function like `add` will have `op1`, `op1` and `sum` as parameters (and `2`, `2` and a variable as aguments), yet returns a list with a single tuple: `(2, 2, 4)`. A query function always returns a list of tuples.

The write function writes the tuple to the database (a database and table of its own choosing).

## Atoms

The instance of a relation is called a tuple, but in this library the tuple is extended with some other characteristics and this warrants another name. An **atom** is thus a tuple (as **arguments**) along with a **predicate**, a **determiner** and **modifiers**.

## Davidsonian event-semantics

Davidsonian semantics treats the **instance** of a verb as a separate parameter to the relation. Usually the first.

In stead of `push(john, david)` you would use `push(E1, john, david)`. This allows you to reason over the event instance. It allows you to add adverbs (`quickly(E1)`), which is important in story telling, and you may connect events to form causal chains.

The library often uses Davidsonian semantics in its examples, because it is a more compact than Neo-Davidsonian semantics, and is more in line with how entities are usually stored in a relational database.

## Neo-Davidsonian event-semantics

Davidsonian semantics is the more **extreme form**. It treats the event parameter as the only parameter.

In stead of `push(john, david)` you would use `push(E1), agent(E1, john), patient(E1, david)`. The advantage is that you don't need to consider which parameters are "essential" to the relation, and you can give every parameter an explicit **role**. Disadvantages are that roles are often arbitrary, and that working with it requires more code.

Neo-Davidsonian is possible with the library, and you may have good reasons to use it.

## Classical (non-Davidsonian) semantics

Some applications have no use at all for event instances. That's fine too. You are not required to add an event parameter.

Just use `push(john, david)`.

## Dialog

The library is developed by replicating more and more historical natural language systems. These systems contain sample dialogs between a human and a computer. The dialogs are here implemented in the form of tests, so that they can be replayed automatically and ensure that no bugs are introduced that fail existing dialogs.

## Dialog entities

**Dialog entities** are entities (or rather instances) that play a role in the dialog. Also named **discourse referents**.

## Binary / 3-Valued logic

The default logic of the library is binary, as you're used to. It deals with the values `true` and `false`. It assumes a **closed world** hypothesis: that which is not present in any data source, is assumed not true. While binary logic is much easier to use than trinary logic (with `true`, `false`, and `unknown`), there are cases in which the latter is needed. In the **Cooper** demo this scenario is worked out. It uses **open world** relations, that always succeed.

## Intents

An **intent** is the relation that performs the main function of a sentence. Intents are often connected with specific keywords in sentence, like `what`, `why` and `how many`. The need to resolve specific entities from a sentence and return the results in some specific way.

## Semantic grammar

A semantic grammar is a grammar that contains the names of relations and entities in its syntactic rules. For example

    s -> 'what' 'is' aggregate element 'in' material

The categories `aggregate`, `element` and `material` are not syntactic, like `noun` and `verb`.

The current library allows you to create a semantic grammar, and there are some good use cases for it. But you must be aware that the grammar you build is very domain-specific and there's a low chance of being able to reuse it in other projects.

Adding some semantic grammar elements to any grammar is normal, however.
