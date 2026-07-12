The library is being designed to be simple to use and support a wide range of language and cognitive skills.

This page describes the core concepts of the library.

## A basic system, extended by modules

The basic system just has a parser, a composer, and an executor. Everything else is done by (external) modules. This makes it lightweight, extendible, and easier to understand and test. Some modules are linked rather directly to the system, but the interaction is minimal, and uses interfaces.

## A simple grammar formalism

The library uses **Entity Unification Grammar**, a formalism I developed to make semantic composition easy. Easier, that is, than [Montague grammar](https://en.wikipedia.org/wiki/Montague_grammar) and [Feature Structure Unification](https://en.wikipedia.org/wiki/Feature_structure), in the sense that the cognitive load of developing a new rule is lower: the number of semantic operations is low, and picking the right operator is usually an obvious choice.

It is explained [here](composition.md).

## Start simple, then transform

Historically there are two ways to do syntactic analysis and semantic composition. The first analyses the sentence using a large amount of code that has a strong learning curve. The other uses syntactic rewriting rules, but the semantic composition rules are hard to understand and apply.

This library uses syntactic rewrite rules and has aimed to make the semantic composition as easy as possible. The developer attaches semantic forms to syntactic tree nodes that are just the most basic logical representation.

One of the ways to keep the composition simple is to leave quantification out of the composition process, and offer a built-in function that transforms the structure into a quantified form. The composition, which is done manually is therefore easier, while the transformation is done by the function.

## A complex query is just a composition of simple queries

Where most systems try to create a single SQL statement to execute a sentence, this system breaks the query down to a series of select statements and executes these. The result is not `SELECT COUNT(*) FROM .. JOIN .. JOIN .. GROUP BY ...`; rather all database queries involve only a single table, a few simple selects and some simple where clauses: `SELECT a, b, c FROM t WHERE a = 1 anc c = 2`.

Advantages

- Creating an adapter to a new database is simple
- Custom application logic can be included during the query

Disadvantages

- Doing the work in the application is always slower than letting the database do the work

The advantages may not seem to weigh up against the disadvantages. But consider this. Many natural language sentences can't be solved by a single database query, and require multiple interactions between data access and data processing. That's where this approach shines.

The disadvantage of accessing the database in an inefficient way is tackled by optimizer functions (`OptimizerModule`).
