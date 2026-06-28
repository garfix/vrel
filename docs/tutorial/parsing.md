# Parsing

Before we get into semantics, we need to learn about tokens and parse trees.

A __tokenizer__ breaks a sentence up into smaller parts, __tokens__, which form the input to the parser. As an example sentence let's take "John loves Mary". A tokenizer could cut up the sentence into the tokens `John`, `loves`, and `Mary`. However, this would limit the analysis to the word level, and would require another analyser to analyse the morphemes of a word. This system combines parsing and __morphological analysis__ and to that end it splits the sentence into characters: `J` `o` `h` `n` ` ` `l` `o` `v` `e` `s` ` ` `M` `a` `r` `y` `. Technically, the character is the token, but since there's not much use in that, I call a token a sequence of characters: either a fixed character string or the match of a regular expression.

All whitespace sequences of space, tabs and newlines are replaced by a single space.

A __parse tree__ is a tree-representation of a sentence. This __syntactic__ representation is based on the hierarchical nature of language: a sentence is a compound of phrases, and these phrases are themselves composed of other phrases. A __parser__ parses a sentence to form such a tree. It uses __rewrite rules__ to transform the root node "s" into the branches "np" and "vp". These branches are then themselves rewritten into new branches. It's a recursive process that ends in the words of the sentence.

To see this in action, copy this sample script and run it.

~~~python
from richard.core.System import System
from richard.entity.SentenceRequest import SentenceRequest
from richard.processor.parser.BasicParser import BasicParser
from richard.block.FindOne import FindOne

def parser_demo():

    grammar = [
        { "syn": "s(V) -> np(E1) vp(V, E1)" },
        { "syn": "vp(V, E1) -> verb(V) np(E1)" },
        { "syn": "np(E1) -> noun(E1)" },
        { "syn": "noun(E1) -> proper_noun(E1)" },
        { "syn": "proper_noun(E1) -> 'john'" },
        { "syn": "proper_noun(E1) -> 'mary'" },
        { "syn": "verb(V) -> 'loves'" },
    ]

    parser = BasicParser(grammar)

    system = System(
        model=model,
        input_pipeline=[
            FindOne(parser)
        ],
        output_generator=generator
    )

    request = SentenceRequest("John loves Mary")
    parse_tree = system.enter(request)
    print(parse_tree)


if __name__ == '__main__':
    parser_demo()
~~~

The variables `E1` and `V` that you see after each category within brackets, help to integrate the semantics of child nodes with their parent. You will see how they are important when we get to semantics.

Something about the choice of the rewrite rules that form the grammar: these rules, like `vp -> verb np`, are not the only ones possible. Linguistic frameworks have many ways of decomposing a sentence. Read [Wikipedia on Grammar](https://en.wikipedia.org/wiki/Grammar) for more information. I have not yet found a grammar that fits all purposes, and I will be using slightly different grammar rules throughout this documentation. You may look at [X-bar theory](https://en.wikipedia.org/wiki/X-bar_theory) as matches my approach best. But other types of grammar may be used as well.

An important characteristic of a grammar for a semantic parser is that there are many rewrite rules at the sentence level. The results that a sentence produces largely depend on the top-level construct of a sentence.

This library uses [Earley's parser](https://en.wikipedia.org/wiki/Earley_parser), which is fast and efficient, and doesn't fall into infinite recursion with left-recursive rules (i.e. `a -> a b`). The algorithm is adapted to use spans of tokens (here: characters), rather than work with individual tokens.

You may be missing a lexicon in this example. A __lexicon__ is a collection of all the individual words of a language, together with their meanings. This library integrates the lexicon in the grammar to simplify the definition of idioms. An __idiom__ is a group of words that does not form a phrase but contains a specific meaning. For example: "How many countries have population above 100 million?"

When you run the script, you should see the following parse tree representation.

~~~
s
+- np
|  +- noun
|     +- proper_noun
|        +- john 'John'
+- vp
   +- verb
   |  +- loves 'loves'
   +- np
      +- noun
         +- proper_noun
            +- mary 'Mary'
~~~

## character strings and regular expressions

A character string like 'mary' matches a sequence of 4 tokens: `M`, `a`, `r` and `y`.

In stead of character strings, you can also use a regular expression like `/\w+/` or `/\d+/`.

~~~python
{
    "syn": "proper_noun(E1) -> /\w+/",
    "sem": lambda token: [('resolve_name', token, E1)]
}
~~~

## Token delimiters

The default delimiter between two phrases or tokens is the space ("  "). However, when no space is expected, use the `+` delimiter to glue together two tokens:

~~~python
{
    "syn": "s(E1) -> 'does' np(E1) vp_nosub_obj(E1)+'?'",
}
~~~

The `+` delimiter is essential in analysing morphemes. In this example the plural "s" is simply discarded:

~~~python
{
    "syn": "common_noun(E1) -> common_noun(E1)+'s'",
    "sem": lambda common_noun: common_noun
}
~~~

If a space is optional but not required, use the tilde delimeter: `~`:

~~~python
{
    "syn": "s(E1) -> 'does' np(E1) vp_nosub_obj(E1)~'?'",
}
~~~

This says: the sentence ends with a question mark, possibly preceded by space.

## Optional tokens

A token can be made optional by adding a "?" after it.

~~~python
{
    "syn": "s(E1) -> np(E1) 'is' 'a'? 'part' 'of' np(E2)",
}
~~~

This will match both "is a part of" and "is part of".

## Morphological analysis

The following rules ignore the plural suffix "s". The first rule is the common rule. The second one is for words that end with "ies": cities -> city.

~~~python
{
    "syn": "noun(E1) -> noun(E1) + 's'",
    "sem": lambda noun: noun
},
{
    "syn": "noun(E1) -> /\w+/ + 'ies'",
    "sem": lambda token: [(token+'y', E1)], "dialog": lambda token: [('dialog_isa', e1, token+'y')]
}
~~~

## Multiple parse trees

Even if the input consists of multiple sentences, the default output of the parser is a single tree with `s` as the root category.
It's possible to produce multiple parse trees; one for each sentence. In this case, specify the categories that form the root categories of these trees.

~~~python
parser = BasicParser(read_grammar, sentence_categories=["decl", "question"])
~~~

In this example, the topmost occurrences of the specified categories will serve as sentence roots.

## Parse tree pruning

After all parse trees have been extracted, there are many meaningless trees that were formed by the regular expression rules that could be applied on about any word. To get rid of these meaningless parse trees, only the ones with **the least amount of regexp nodes** are kept.

## Parse tree ordering

A bigger grammar will produce more parse trees. The most important factor for __ambiguity__ is the use of the __token__ category in a rewrite rule, since it matches any word.

The pipeline will try the alternative parse trees one by one, starting with the one that happens to be the first to be produced. Without support, the order of the parse trees would only be influenced by the order of the rewrite rules in the grammar. Depending on this can be tricky and in some cases it is impossible to have the right interpretation come up first.

That's why the parser is equuipped with a few sorting heuristics that help place the best tree up front. These heuristics, combined in `BasicParseTreeSortHeuristics` produce a reasonable result, but you may find it insufficient. It may be needed to replace these basic heuristics with your own.

## Sort by tree depth

The first heuristic sorts parse trees by decreasing tree depth. The most deeply nested sentence is placed first. To illustrate this idea, take the following sentence

> What are the continents no country in which contains more than two cities whose population exceeds 1 million?

It can be parsed (among many others) like this

~~~text
What are the continents
             + no country in which contains more than two cities
             + whose population exceeds 1 million?
~~~

and like this

~~~text
What are the continents
             +  no country in which contains more than two cities
                                                       + whose population exceeds 1 million?
~~~

The clause that starts with "whose" can modify either "continents" or "two cities". The latter is a more likely interpretation, since this np is nearer.

I don't know of any literature that supports this claim, however. Let me know if you know of any.

## Sort by token count

The category `token` is used for proper nouns and other entities that can't be listed in full in the lexicon. It matches any token. A grammar with more tokens will create more parse trees and make it accept more sentences. However, when execution starts these tokens are turned into names to be resolved. A sentence with many random tokens will fail. A sentence with the least amount of tokens has the best chance of succeeding and is therefore placed up front.

## Sort by boost

When you __just know__ that one interpretation of a sentence should be preferred over the other, you can "boost" that sentence, like this:

~~~python
{
    "syn": "s(E1) -> 'what' 'are' np(E1) '?'",
    "sem": lambda np: apply(np, []),
    "dialog": [("format", "list"), ("format_list", e1)],
},
{
    "syn": "s(E1, E2) -> 'what' 'are' 'the' noun(E1) 'of' np(E2) '?'",
    "sem": lambda noun, np: noun + [('of', E1, E2)] + apply(np, []),
    "dialog": [("format", "table"), ("format_table", [e2, e1], [None, None])],
    "boost": 1
}
~~~

The sentence "What are the capitals of european cities?" is matches by both rules, but the second one is more specific and should be preferred. Therefore it is boosted. The default boost value is 0. Multiple boost values can be used if needed.
