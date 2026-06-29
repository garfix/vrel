# Execution

Once the composer has composed the semantic representation in the forms of a list of logical atoms, like this

```prolog

    ('ocean', $1)
    ('borders', $1, $2)
    ('african', $2)
    ('country', $2)
    ('borders', $1, $3)
    ('asian', $3)
    ('country', $3)

```

the executor (`AtomExecutor`) is able to execute it. Execution is similar to the logic programming language [Prolog](https://en.wikipedia.org/wiki/Prolog). It starts out with an empty variable binding. Then processes the list of atoms, one by one. Each free variable is bound to one or more values. If the atom has a variable that is already bound, this variable value is used as a restriction to the atom.

In the above example the first atom is `('ocean', $1)`. It contains the new variable `$1`. The **predicate** `ocean` is sent to one of the available modules that is able to process it (there may even be multiple modules that can process it). The module returns a list of values for the variable. `$1` is then bound to `arctic_ocean`, `indian_ocean`, `pacific` etc. In the next atom, `('borders', $1, $2)`, `$1` is already bound, and the module that handles the predicate `borders` is given a bound value of `$1`. It then finds the values of `$2`, given the bound value of `$1`. When no values are found for an atom, the process stops and the result is an empty list of bindings. If the list completes, the executor returns a list of distinct bindings. Each binding has a value for `$1`, `$2` and `$3`.

Some predicates handle lists of atoms for an argument. For example

```prolog
('count', $4, [
    ('ocean', $1)
    ('borders', $1, $2)
])
```

performs the body `('ocean', $1) ('borders', $1, $2)` and counts the number of results and returns this as `$4`.

## Solver

The executor doesn't execute the list of atoms by itself. It orders the `Solver` to do so. The solver is a lightweight object that gains its power from the fact that it has access to all modules of the model.

The solver goes through the atoms one by one, executing it and collecting its result bindings. Each binding is then passed to the next atom as input. If an atom gives no results, the solver returns an empty list. If all atoms succeed, the solver returns a list of all bindings.

## ExecutionContext

The solves queries the model for all modules that implement a relation. Each relation has `query_function`. This function is called by the solver. The solver passes the current variable bindings as values to the function and expects a list of new values. But it provides more to the relation, because relations can have a wide variety of functions.

The execution context contains

- relation: Relation
- predicate: str
- arguments: list
- binding: dict
- solver: SomeSolver

`relation` is the Relation object of the relation. `predicate` is the predicate (name) of the relation. `arguments` is the list of arguments **before binding the variables**, so it still contains the variables of the atom. `binding` is the current set of variable-value pairs. `solver` is a reference to the solver. It can be used by the relation to solve lists of atoms by itself.

When a query function is called, the solver passes both the bound arguments (where variables are replaced by their current values) as `db_values`, and the execution context. Most relations just use the current values. The context is used for a variety of special relations.

## Processing exception

When a relation handler finds a problem that can't be resolved within the process, yet needs to be communicated with the user, the handler may raise a `ProcessingException` with a message. This message will be part of the result of the process and the block, and will end up in the response to the user.

An example is handling `resolve_name`. If the name can't be found, there's no use returning an empty list as this will result in an empty response and this is not useful to the user. In stead the handler can raise a `ProcessingException` with the message: "Name not found: ..."
