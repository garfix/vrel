from vrel.core.constants import AUTO, E1, E2, E3, E4, E5, UNKNOWN_PREDICATE
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable


T1 = Variable("T1")
T2 = Variable("T2")
T3 = Variable("T3")


def get_read_grammar():

    return [
        # sentence
        # magnesium is a metal
        {
            "syn": "s() -> proper_noun(E1) 'is' a() np(E1, T1)",
            "sem": lambda proper_noun, a, np: [Atom("intent_tell", [proper_noun, np], T1)],
        },
        # magnesium burns rapidly
        {
            "syn": "s() -> noun(E1, T1) verb(E1)",
            "sem": lambda noun, verb: [Atom("intent_tell", [Atom(verb, noun, T1)], T1)],
        },
        # np
        {"syn": "np(E1, T1) -> noun(E1, T1)", "sem": lambda noun: noun},
        # verb
        {
            "syn": "verb(E1) -> 'burns' 'rapidly'",
            "sem": lambda: "burns_rapidly",
        },
        # article
        {"syn": "a() -> 'a'", "sem": lambda: []},
        {"syn": "a() -> 'an'", "sem": lambda: []},
        # noun
        {
            "syn": "noun(E1, T1) -> common_noun(E1, T1)",
            "sem": lambda common_noun: common_noun,
        },
        {
            "syn": "noun(E1, T1) -> proper_noun(E1)",
            "sem": lambda proper_noun: proper_noun,
        },
        # common noun
        {"syn": "common_noun(E1, T1) -> 'metal'", "sem": lambda: Atom("metal", E1, T1)},
        # proper noun ("magnesium")
        {
            "syn": "proper_noun(E1) -> /\\w+/",
            "sem": lambda token: Atom("name", E1, token),
        },
    ]
