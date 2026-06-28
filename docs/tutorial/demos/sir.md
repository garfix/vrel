# SIR

Replicates a dialog of SIR (Semantic Information Retriever), by Bertram Raphael as described in "SIR: a computer program for semantic information retrieval" - Bertram Raphael (1964)

## Learning concepts

SIR has no built-in nouns. They're all taught by the user. The identifier of the concept is simply it's word in the sentence. The singular is taken, and therefore it's needed to split a word in its root morpheme and its plural suffix ("s").

## Teaching is-a relationships

SIR contains sentences like "Every boy is a person". These are added to the database in the form `isa('boy', 'person')`.

The page [is-a relationships](../language/is-a.md) has more on the topic.

## Teaching equality

SIR contains sentences like "John is Jack". These are added to the database in the form `equals('John', 'Jack')`.

The page [is (equals)](../language/is-equals.md) has more on the topic.

## Teaching concepts

SIR teaches the structure of concepts Notice these sentences:

    A finger is a part of a hand
    Every hand has 5 fingers

The first sentence just describes the relationship between finger and hand. The second sentence does the same, but adds the fact that there's number involved. In the demo these relationships are implemented by the predicates `part_of` and `part_of_n`.

## Clarification comments

SIR tells the user what knowledge is missing to make the proper inference. It can respond with "Don't know whether finger is part of John" and "How many finger per hand?". This is implemented in the predicates `have` and `part_of_n`. If they don't yield any results, the raise the exception that forms the response.

The implementation of this feature is very brittle. Simple changes to the inferences can break it.

## Checking declarative statements

When the user makes a statement "The pad is to the left of the telephone", this information is not added to the database right away. It is first checked for consistency with the existing information. If the pad is already found to be to the right of the telephone, the system will respond "The above statement is impossible".

## Exceptions to the rule

SIR is told how many a fingers a person has in general, and also how many fingers Tom has:

* There are two hands on each person. Every hand has 5 fingers.
* Tom has 9 fingers

When asked "How many fingers has Tom?" SIR could find both "10" and "9" as the answer. However, it first tries to determine to look up the answer, and only if that fails, it tries to find the answer by reasoning.

The disjunctive operator in Prolog can be used for this kind of reasoning:

~~~pl
part_of_number(A, B, N) :- (
    # direct, non inheriting
    part_of(A, B), part_of_n(A, B, N)
;   # direct, inheriting
    full_isa(AA, A), full_isa(B, BB), part_of(AA, BB), part_of_n(AA, BB, N)
;   # transitive, non inheriting
    part_of(C, B), part_of(A, C), part_of_n(C, B, N1), part_of_number(A, C, N2), multiply(N1, N2, N)
;   # transitive, inheriting
    full_isa(B, BB), part_of(C, BB), part_of(A, C), part_of_n(C, BB, N1), part_of_number(A, C, N2), multiply(N1, N2, N)
).
~~~

The Prolog `;` separates the possible solutions. The second disjunct is only executed when the first fails, and so on.

## Using context

In SIR the predicate `left_of` should just mean the simple look-up of the fact when creating output, but it should be transitive in the case of a question.

The context module has a means of starting a context in the dialog. This for example how to start a context called "question":

~~~python
[('with_context', 'question', [('intent_yn', proper_noun1 + proper_noun2 + preposition)])]
~~~

This context can be used by inference rules:

~~~pl
# in the context of a question, left_of is transitive
left_of(A, B) :- context('question'), just_left_of(A, B).
left_of(A, B) :- context('question'), just_left_of(A, C), left_of(C, B).
left_of(A, B) :- context('question'), just_left_of(C, B), left_of(A, C).
~~~

Todo: the syntax of the context in the inference should be simpler
