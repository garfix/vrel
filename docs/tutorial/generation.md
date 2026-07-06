## The basics

In **response generation** a response sentence is generated based on rewrite rules and data source data.

The relation `output_type` that is filled by the intent handler provides the main input to generation. After that, any data may serve as condition for further rewrites.

Generation takes place based on rewrite rules that take a category as a head, and one or more categories as body. In the following example the head is `s` and the body `np` and `vp`.

Each sentence starts out with a `s` category. The generator looks for rules with `s` as its head and that match the `if` condition. The first rule (from top to bottom) that matches is used. The sentence that first look something like "s()" is now rewritten to something like "np() vp()", and the `np` and `vp` will be rewritten further.

Note that the variables `E1` and `E2` that are bound during the condition matching process, are used as arguments to the `np` and `vp` categories, and will be passed to the new rules as input.

```python
{
    "syn": "s() -> np(E2) vp(E1)",
    "if": [
        Atom("output_type", "declarative"),
        Atom("output_subject", E1, E2),
    ],
},
```

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

## Order of execution

At some point you may want to know exactly what happens in what order. The generator processes a rule like this:

- match the head along with its arguments
- execute the `if` clause and keep the variable binding
- if the rule contains a `list_element` variable, this variable is assumed to be a list, and the following steps are repeated for each element in the list. Together they will form a `list_result`. Otherwise, they are executed just once
  - each of the consequent categories is processed in a recursive way, by this same process
  - the result of these consequents are combined by the `combine` function, if available. Otherwise any `None` values are removed, they're converted to strings, and concatenated.
  - the resulting string is postprocessed by a `post` function, if available
- if the rule contains a `list_element` variable, and a `list_combine`, the `list_combine` takes the `list_result` as input and return the output.

## Literal

A value that is to be displayed as-is, can be produced using the category `literal`.

```python
{
    "syn": "s() -> 'The answer is' literal(E1)",
    "if": [Atom("output_type", "count"), Atom("output_count", E1)],
},
```

## Format

You can use the category `format` to use a custom function to create a result.

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
    "if": [Atom("output_type", "list"), Atom("output_list", E1)],
    "list_element": E1,
    "list_combine": lambda nps: ", ".join(nps),
},

```

## Combine

The `combine` function tells the generator how the results of the body nodes are to be combined. Without a `combine` function, the results are cast to strings, any `None` values removed, and concatenated. The `combine` function may change that:

```python
{
    "syn": "s() -> format(E1, E2)",
    "if": [Atom("output_type", "table"), Atom("output_table", E1, E2)],
    "format": lambda results, units: format_table(results, units),
    "combine": lambda table: table,
},
```

Here the consequents are not combined and turned into a string, but just passed on as an array.

## Post

`post` is executed last and adds simple string based processing, like `strip`.

```python
{
    "syn": "s() -> custom()",
    "post": lambda custom: custom.strip()
},
```
