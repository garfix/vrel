# Cooper's system

This demo replicates a dialog of William S. Cooper's system as described in "Fact Retrieval and Deductive Question-Answering Informatlon Retrieval Systems" - Cooper (1964)

The main features of this model are:

- Use of three-valued logic (true, false, unknown); a open world assumption
- Learning names of things
- Learning simple rules about things

The open world assumption is not mentioned in the article, and the concept is neither explicitly mentioned nor essential for the system. I choose 3-valued logic because I thought it was in the spirit of the system, and that this would be a good opportunity to experiment with it. I found it hard, to be honest. For one, I had to find out how to do 3-valued logic. This included creating the 3-valued variants of `not` and `and`, as well as being able to store both negative and positive facts in a database. I don't recommend using this experiment as the basis for your own system, unless you have a good reason to distinguish between `false` and `unknown`, or you just want to experiment with this kind of logic.

Clone the repository to view and run the demo. The code can be found in `tests/integration/cooper/test.py`

## Three-valued logic

The main logic of Vrel, like Prolog, is based on treating the absense of a fact as treating it as false. This is called the **closed world assumption**: the assumption that all that is known about a subject is present in the database.

Cooper's system works differently. A fact can be available positively (`true`), or it can be available negatively (`false`). If neither is the case, the fact is `unknown`.

All predicates in this replication have an extra truth-value `truth` that can be `true` or `false`. This tuple, for example, expresses the fact that it not true that gasoline burns rapidly.

    burns_rapidly('gasoline', 'false')

The replication has logical operators that handle tree-valued logic:

    not_3v(T1, T2)

`T2` results in the negative of `T1`, where `T1` may be "unknown". The negative of "unknown" is "unknown".

    and_3v(T1, T2, T3)

`T3` results in the logical `and` of `T1` and `T2`. If either `T1` or `T2` is "unknown", the result `T3` is "unknown".

The result of evaluating a sentence in the second grammar is also a truth value. Whereas a regular grammar in our system passes entities around, this replication also passes truth values around. This is not a problem because truth values are entities as well.

## Two types of entities

This implementation of Cooper deals with two types of entities.

The first one are classes like `oxide` that are known in advance, and are treated as `np`'s.

The second one are instances like `sulphur oxide` that are introduced in the dialog and are treated as `proper nouns`.

In this system proper nouns are not np's, for simplicity's sake.

## Same as

Cooper has sentences like "salt is natrium chloride". These are implemented by adding a record to the `same_as` relation. Both entities have different id's, and are linked through that relation.

A `SameAsHandler` is added to the model so that the solver can treat multiple id's as the same.

## Preventing stack overflow

Cooper has the sentence "every oxide is an oxide", which is added as a rule to the database. Howver, use of the rule causes infinite recursion (`oxide(E, T) :- oxide(E, T)`). A `StackOverflowHandler` is added to prevent this. The solver returns an empty resultset when infinite recursion is detected.

## Learning rules

Cooper's dialog contains sentences like

- no metal is a nonmetal
- combustable things burn

These rules are learned by the system at runtime in order to be used in inferences.

"no metal is a nonmetal" is turned into `nonmetal(E1, 'false') :- metal(E1, 'true').`

"combustable things burn" is turned into `burns(E1, 'true') :- combustable(E1, 'true').`

The inference module has a built-in predicate `learn_rule` for this purpose. It takes a head and body as arguments.

## Rejecting new rules

Cooper's system doesn't just accept any facts or rules the user enters, it first checks if it can find a counter example. If it does, it rejects the rule, and returns `False`.
