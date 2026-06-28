# CHAT-80

Replicates the Chat-80 system by David H.D. Warren and Ferando C.N. Pereira (1981)

This was a popular natural language system at the time, and has even been used in the classroom. It was one of the first systems implemented in Prolog and was in fact intented to display the power of the new programming language.

It's able to handle some quite complex sentences that include several types of sentences (yes/no, numbers, multiple results, table results, and canned responses), subordinate clauses ("that ..."), and superlatives ("largest").

Clone the repository to view and run the demo. The code can be found in `tests/integration/Chat80_test.py`

## Goals and inference

Chat-80 is built completely in Prolog. The language is not very popular any more, but the concept of handling a tuple as a __goal__ that can be achieved by fulfilling its __subgoals__ is still very useful. This aspect has been replicated in this system in the form of inference rules that use a basic subset of the Prolog language:

~~~prolog
in(A, B) :- contains(B, A).
in(A, B) :- contains(C, A), in(C, B).
~~~

In this example, the predicate `in` implements the geographical contains-relation. It is solved by inference. Two rules apply to this predicate, and both are executed to yield answers. Note also that the second rule is recursive.

Inference is described [here](../modules/inference-engine.md)

## Query optimization

Chat-80 is unique (afaik) in that it has built-in query optimization functionality. The declarative semantics makes it possible to restructure the query after it has been formed. When the authors found that the queries took minutes to execute, they looked for the cause and worked out two elaborate algorithms to optimize the query:

- sort by cost
- isolate independent parts

These are described [here](../introduction/composition.md)

## References

The dialog replicated can be found [here](https://github.com/JanWielemaker/chat80/blob/master/prolog/chat80/demo)

CHAT-80 is mainly described in

- Efficient Processing of Interactive Relational Database Queries Expressed in Logic - Warren (1981)
- An efficient easily adaptable system for interpreting natural language queries - Pereira, Warren (1982)

