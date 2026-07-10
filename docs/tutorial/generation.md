## The basics

In **response generation** a semantic expression is turned into a natural language sentence in order to be shown to the user. It is based on rewrite rules and data source data.

An application uses the relation `out` to store the information that should be output to the user, in the form of a tuple that starts with a output type. The generator uses the relation `last_output` to read the last output tuple available.

Here's an example of a semantic expression the application whats to output. It's a clariying expression that asks the user for information.

```python
out('how_many', E1, E2)
```

this expression can be handled by this rule

```python
{
    "syn": "s() -> 'How many' thing(E1) 'per' thing(E2)+'?'",
    "if": [Atom("last_output", "how_many", E1, E2)],
},
```

Generation takes place based on rewrite rules that take a category as a head, and one or more categories as body. In the following example the head is `s` and the body categories `np` and `vp`.

Each sentence starts out with a `s` category. The generator looks for rules with `s` as its head and also match the `if` condition. The first rule (from top to bottom) that matches is used. The others are skipped. The sentence that first looks something like "`s()`" is now rewritten to something like "`np()` `vp()`", and the `np` and `vp` will be rewritten further.

```python
{
    "syn": "s() -> np(E2) vp(E1)",
    "if": [
        Atom("last_output", "declarative", E1, E2),
    ],
},
```

Note that the variables `E1` and `E2` that are bound during the condition matching process, are used as arguments to the `np` and `vp` categories, and will be passed to the new rules as input.

`vp` may rewrite to `verb` and `verb` can have a rule like this

```python
{
    "syn": "verb(E1) -> 'starts'",
    "if": [
        Atom("start", E1, E2),
    ],
},
```

which produces the word `starts`.

## Literal

A value that is to be displayed as-is, can be produced using the category `literal`.

```python
{
    "syn": "s() -> 'The answer is' literal(E1)",
    "if": [Atom("last_output", "count", E1)],
},
```

## Format

You can use the category `format` to use a custom function to create a result. This function is provided in the rule via the key "format".

```python
{
    "syn": "things(E1) -> format(E1)",
    "format": lambda things: format_list(things)
},
```

## Handle lists of values

When a variable contains a list of values, and each of the values needs to be rewritten separately, you can use the `list_element` and `list_combine` items.

```python
{
    "syn": "s() -> np(E1)",
    "if": [Atom("last_output", "list", E1)],
    "list_element": E1,
    "list_combine": lambda nps: ", ".join(nps),
},
```

In this example the result is an enumeration of names, separated by commas.

## Combine

The `combine` function tells the generator how the results of the body nodes are to be combined. Without a `combine` function, the results are cast to strings, any `None` values removed, and concatenated. The `combine` function may change that:

```python
{
    "syn": "s() -> format(E1, E2)",
    "if": [Atom("last_output", "table", E1, E2)],
    "format": lambda results, units: format_table(results, units),
    "combine": lambda table: table,
},
```

Here the consequents (the output of `format`) are not turned into a string, but just passed on as an array.

## Post

`post` is executed last and adds simple string based processing, like `strip`.

```python
{
    "syn": "s() -> custom()",
    "post": lambda custom: custom.strip()
},
```

## Order of execution

At some point you may want to know exactly what happens in what order. The generator processes a rule like this:

- match the head along with its arguments
- execute the `if` clause and keep the variable binding
- if the rule contains a `list_element` variable, this variable is assumed to be a list, and the following steps are repeated for each element in the list. Together they will form a `list_result`. Otherwise, they are executed just once
  - each of the consequent categories is processed in a recursive way, by this same process
  - the result of these consequents are combined by the `combine` function, if available. Otherwise any `None` values are removed, they're converted to strings, and concatenated.
  - the resulting string is postprocessed by a `post` function, if available
- if the rule contains a `list_element` variable, and a `list_combine`, the `list_combine` takes the `list_result` as input and return the output.
