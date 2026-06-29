# Semantic composition

The meaning of a sentence or phrase can be composed of the meaning of its constituent phrases. Known as [Frege's principle](https://en.wikipedia.org/wiki/Principle_of_compositionality), this is the basis of deriving the meaning of a sentence.

## Semantic attachments

A grammar rule can be extended with a **semantic attachment**, expressed by the "sem" key of a syntactic rule, which expresses the meaning of the phrase covered by the rule. In this library the attachments take the form of lists of atoms. The atom is implemented as a Python tuple.

An atom is a combination of a predicate with some arguments. Examples are `Atom('river', E1)`, `Atom('give', E1, E2, E3)`. The arguments may be variables (as in the example) or values.

Most sems are lists of atoms. This allows us to combine sems by simply adding the lists. Sems that don't need to be combinable can just be single atoms, or even simple values.

## Adding semantics to the syntax rule

Here are example rules that demonstrate the typical 2-part structure of a semantic attachment ("sem"):

```python
{
    "syn": "noun(E1) -> 'rivers'",
    "sem": lambda: Atom('river', E1)
},
{
    "syn": "vp(E1) -> verb(E1, E2) np(E2)",
    "sem": lambda verb, np: verb.mod(np)
},
```

Notice that "sem" is formed by a lambda function that returns an atom.

The function `lambda verb, np: ...` is used to import the semantic values of the child nodes. Each child value is appointed a parameter with the same name as the syntactic category it belongs to. In the example above, `verb` is the first consequent of the rule, and `verb` is therefore the name of the first parameter of the function. In the same way, `np` is the second consequent, and therefore the second parameter. Only categories need parameters. Words (like `'river'` or `'two'` have no need for a parameter, as they have no child nodes).

The parameter names are not required to be the same as the syntactic categories, but it is good practice to keep them that way. An exception occurs when the rule has two of the same syntactic categories, as in `term -> term operator term`. In this case append a follow-up number, like `lambda term1, operator, term2`.

The returned value, an atom like `Atom('river', E1)]`, forms the real meaning of the rule. It uses the meanings of its child nodes that were made available through the parameters of the function.

## Three composition operations

Calculating the semantics of a phrase is done by three operations: **terminal**, **argument**, **modifier**, **determinater** and **inheritance**.

**terminal** attaches an atom or a literal to a node.

```python
{"syn": "noun(E1) -> 'continents'", "sem": lambda: Atom("continent", E1)},

{"syn": "number(E1) -> 'three'", "sem": lambda: 3},
```

**argument** introduces an atom and uses the semantics of its children as arguments.

```python
{
    # Which countries are bordered by two seas?
    "syn": "s(E1) -> 'which' nbar(E1) 'are' vp(E1) + '?'",
    "sem": lambda nbar, vp: Atom("intent_list", E1, [nbar, vp]),
},
```

**modifier** modifies one child node with another child node. Any amount of modification may be done by a single rule.

```python
{"syn": "nbar(E1) -> adjp(E1) nbar(E1)", "sem": lambda adjp, nbar: nbar.mod(adjp)},

{
    "syn": "relative_clause(E1) -> np(E2) preposition(E2, E1) 'which' vp(E2)",
    "sem": lambda np, preposition, vp: vp.mod(np.mod(preposition)),
},
```

**determiner** adds a determiner to an atom.

```python
{
    "syn": "np(E1) -> det(E1) nbar(E1)",
    "sem": lambda det, nbar: nbar.with_determiner(det),
},
```

**inheritance** is the simplest operation. The semantics of the parent node are identical to the semantics of its child node.

```python
{"syn": "np(E1) -> nbar(E1)", "sem": lambda nbar: nbar},
```

## Query optimization

The composition phase results in a list of atoms. Some of these contain a list of atoms as their arguments themselves. These atoms are about to be executed in order to process the sentence. The atoms form the meaning of the sentence and when executed they perform the function of the sentence. But is this an _efficient_ implementation of the function? Is it fast?

This system, like Prolog, processes atoms (called "goals" in Prolog) one by one. Each atom can either increase or decrease the number of variable bindings. Each of these bindings is then used as input to the subsequent atoms.

David Warren, one of the pioneer of the Prolog language, and together with Fernando Pereira designer of the famous Chat-80 system, recognized that the inference rules of Prolog are logically sound, but suffer from two performance problems. In the article "Efficient processing of interactive relational database queries expressed in logic" he worked out two ways to overcome them. Both of them have been implemented in the current system, as `BasicQueryOptimizer` which can be added to the composer as `query_optimizer`.

### Place resolve_name atoms up front

But let's start with an optimization I added myself. I added `FrontResolveName`, an optimizer that puts all `resolve_name` atoms in the list up front. In most cases a name resolver yields only one or just a few results. Best to place these atoms up front.

### Sort by cost

Warren's first optimization is named "ordering goals in a conjunction" and implemented here by `SortByCost`. The basic idea is that an atom that creates less variable alternatives should be placed before an atom that creates more alternatives. The first one "costs less". Cost is determined by the number of tuples in the relation denoted by the predicate of the atom: the **size** of the relation. Larger relations cost more. But that is not all. Once an argument of the atom is bound, the situation changes as the number of values produced changes quite a bit. How much this number changes depends on the number of different values of the argument: its **cardinality**.

In Warren's example a relation "borders" has a size of 900 tuples. Each of its arguments has cardinality 180. (There are 180 countries which are bordering in 900 different ways) When none of its arguments are bound, the cost of the atom is simply 900. When one argument is bound, the cost reduces to 900/180 and when both arguments are bound the cost reduces even further, to 900/180/180.

While the outcome of any ordering is the same, the performance of an query sorted by cost can increase dramatically.

Atoms that represent database relations are the main candidates for sorting by cost. Other atoms often depend on other atoms. For example `('>', E1, E2)` should not move to a front position. It should only be used if both E1 and E2 are bound.

### Isolating subqueries

The second optimization is named "isolating independent parts of a query" and implemented here by "IsolateIndependentParts". The problem is best described by Warren himself: "The problem is essentially that resolution treats all goals in a conjunction as being dependent. This is fine so long as the goals share uninstantiated variables. However when two parts of a conjunction no longer share variables, they should be solved independently."

The best illustration of the problem is in this sentence: "Which is the ocean that borders african countries and that borders asian countries?" which translates to

```prolog
answer(X) :- ocean(X), borders(X, C1), african(C1), country(C1), borders(X, C2), asian(C2), country(C2).
```

You can see the similar structures for african and asian countries. The crux is in the fact that C2 is evaluated not once, but for each separate binding of C1. This is inefficient and unnecessary.

Warren didn't give an algorithm for this optimization. It is available in the Prolog code of Chat-80, for the enthusiast. I attempted an implementation based on the numerous examples he gave and I will try to give a bit of an explanation. First I create a dependency graph that links each atom to all other atoms that use the same variable(s). The order of the atoms is retained, and this is important because it the result of earlier optimizations. From this first graph I create a second graph. All atoms are processed anew. If an atom is "global" (it is needed for the response of the sentence), it's made to be independent on other atoms. If the atom has a dependency on a succeeding atom, it is also made to be independent. Otherwise, it is made to be dependent on the first atom it depends on. From this second graph the new query is generated, where each isolated subquery is placed in the body of an `isolated` atom. This kind of predicate executes all atoms in its body, but returns only a single value.

```

```
