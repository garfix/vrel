## Arguments and modifiers

An atom has arguments and modifiers. Modifiers modify the meaning of an atom. An argument can be a variable, a constant, or a list of atoms. A modifier can just be an atom.

There can be multiple ways to define meaning, but this document describes the preferred way. Modelling meaning in a single way keeps the code consistent and predictable. This representation is aimed to allow for easy treatment of questions, commands and statements, assuming simple means to transform this basic structure into structures suitable these speech acts.

Main rule:

- A structure is only added as an argument when this is essential for the use of the predicate's execution.

Argument structures are not serialized, so for the sake of fast queries, structures are kept out of arguments as much as possible. Only if the structure is part of the function's execution plan should it be included as argument.

Another way of saying: the order of the atoms should not matter for the result of the outcome (in terms of data, disregarding speed of execution). If an atom depends on another atom's execution, that atom should be used as an argument.

Effects:

- Verbs use variables for arguments. Position: ususally `any`.
- Nouns use variables for arguments
- Determiners are attached to nouns
- Superlatives use atoms for arguments, as this is required for querying
- `and` / `or` have structures as arguments. There are no meaningful variables. To `or` the arguments are essential, and to `and` it doesn't matter as it is removed anyway.
- relative clauses and other typical modifiers are added as modifiers.
- prepositions use variables

## Verbs

The meaning of a can be defined by a single rule

```
s(E1) -> np(E1) verb(E1, E2) np(E2)
```

or by multiple rules

```
s(E1) -> np(E1) vp(E2)
vp(E1) -> verb(E1, E2) np(E2)
```

In both cases the meaning of the verb is defined as a list of variables.

```
Atom(predicate, E1)
Atom(predicate, E1, E2)
Atom(predicate, E1, E2, E3)
```

Modifiers of a verb are linked to an entity variable.

```
.any(E1, np1)
.any(E1, np1).any(E2, np2)
```

for example

```
s(E1) -> np(E1) vp(E2)
    vp.any(E2, np)

vp(E1) -> verb(E1, E2) np(E2)
    Atom(verb, E1, E2).any(E2, np)
```

## Commands and stories

Commands and story sentences are similar in that they prefer the hierarchical structure

`create_command` transforms the basic sentence molecule by replacing argument variables by modifiers.

```
Atom(verb, E1, E2).any(E1, np1).any(E2, np2)
```

becomes

```
Atom(verb, [np1], [np2])
```

Determiners are left as is.

## Queries

`create_query` transforms it by serializing

```
Atom(verb, E1, E2) np1 np2
```

and by creating determiner transformations

```
Atom(predicate, E1).with_determiner(Atom('all'))
```

becomes

```
Atom('all', E1, [
    Atom(predicate, E1)
])
```

## Factual statements

`create_records` transforms by serializing

```
Atom(verb, E1, E2) np1 np2
```

It can't handle deteriners and ignores them.
