You need to understand some concepts in the field in order to use the library.

## Entities and relations

The common name for anything that can be instantiated is an **entity**. `Person`, `dog`, `employment`, `birthday`, etc. A **relation** is a meaningful, named group of entities: `owns`, `parent`, `caused_by`. "meaningful" here means that it has some function in the application.

A relation is named by its **predicate** (`person`, `owns`, etc) and its **(formal) parameters**. An instance of a relation is a **tuple** and the instances of parameters are called **arguments**.

| abstract  | concrete |
| --------- | -------- |
| entity    | instance |
| relation  | tuple    |
| parameter | argument |

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
