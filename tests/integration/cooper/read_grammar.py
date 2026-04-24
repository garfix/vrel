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
            "syn": "s() -> proper_noun(E1) 'is' np(E1, T1)",
            "sem": lambda proper_noun, np: [Atom("intent_tell", [proper_noun, np], T1)],
        },
        # gasoline is combustable
        {
            "syn": "s() -> proper_noun(E1) copula() adj(E1, T1)",
            "sem": lambda proper_noun, copula, adj: [Atom("intent_tell", [proper_noun, adj], T1)],
        },
        # magnesium burns rapidly
        {
            "syn": "s() -> noun(E1, T1) vp(E1, T1)",
            "sem": lambda noun, vp: [Atom("intent_tell", [noun, vp], T1)],
        },
        # np
        {"syn": "np(E1, T1) -> a() nbar(E1, T1)", "sem": lambda a, nbar: nbar},
        {"syn": "np(E1, T1) -> 'not' np(E1, T2)", "sem": lambda np: Atom("not_3v", T2, T1).pre([np])},
        {"syn": "np(E1, T1) -> nbar(E1, T1)", "sem": lambda nbar: nbar},
        # nbar
        {"syn": "nbar(E1, T1) -> noun(E1, T1)", "sem": lambda noun: noun},
        {
            "syn": "nbar(E1, T1) -> nbar(E1, T2) 'that' vp(E1, T3)",
            "sem": lambda nbar, vp: Atom("and_3v", T2, T3, T1).pre([nbar, vp]),
        },
        {
            "syn": "nbar(E1, T1) -> adj(E1, T2) nbar(E1, T3)",
            "sem": lambda adj, nbar: Atom("and_3v", T2, T3, T1).pre([nbar, adj]),
        },
        {
            "syn": "nbar(E1, T1) -> adj(E1, T2) thing()",
            "sem": lambda adj: adj,
        },
        # vp
        {
            "syn": "vp(E1, T1) -> verb(E1)",
            "sem": lambda verb: Atom(verb, E1, T1),
        },
        {
            "syn": "vp(E1, T1) -> 'is' adj(E1, T1)",
            "sem": lambda adj: adj,
        },
        # verb
        {
            "syn": "verb(E1) -> 'burn'",
            "sem": lambda: "burns",
        },
        {
            "syn": "verb(E1) -> 'burns'",
            "sem": lambda: "burns",
        },
        {
            "syn": "verb(E1) -> 'burns' 'rapidly'",
            "sem": lambda: "burns_rapidly",
        },
        # article
        {"syn": "a() -> 'a'", "sem": lambda: None},
        {"syn": "a() -> 'an'", "sem": lambda: None},
        # copula
        {"syn": "copula() -> 'is'", "sem": lambda: None},
        {"syn": "copula() -> 'are'", "sem": lambda: None},
        # noun
        {
            "syn": "noun(E1, T1) -> common_noun(E1, T1)",
            "sem": lambda common_noun: common_noun,
        },
        {
            "syn": "noun(E1, T1) -> proper_noun(E1)",
            "sem": lambda proper_noun: proper_noun,
        },
        # adjective
        {"syn": "adj(E1, T1) -> 'white'", "sem": lambda: Atom("white", E1, T1)},
        {"syn": "adj(E1, T1) -> 'metallic'", "sem": lambda: Atom("metal", E1, T1)},
        {"syn": "adj(E1, T1) -> 'dark-gray'", "sem": lambda: Atom("dark_gray", E1, T1)},
        {"syn": "adj(E1, T1) -> 'combustable'", "sem": lambda: Atom("combustable", E1, T1)},
        {"syn": "adj(E1, T1) -> 'brittle'", "sem": lambda: Atom("brittle", E1, T1)},
        # common noun
        {"syn": "common_noun(E1, T1) -> 'compound'", "sem": lambda: Atom("compound", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'element'", "sem": lambda: Atom("element", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'metal'", "sem": lambda: Atom("metal", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'nonmetal'", "sem": lambda: Atom("nonmetal", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'oxide'", "sem": lambda: Atom("oxide", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'solid'", "sem": lambda: Atom("solid", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'gas'", "sem": lambda: Atom("gas", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'fuel'", "sem": lambda: Atom("fuel", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'fuels'", "sem": lambda: Atom("fuel", E1, T1)},
        # special
        {"syn": "thing() -> 'things'", "sem": None},
        # proper noun ("magnesium")
        {
            "syn": "proper_noun(E1) -> /\\w+/",
            "sem": lambda token: Atom("name", E1, token),
        },
        {
            "syn": "proper_noun(E1) -> /\\w+/ /\\w+/",
            "sem": lambda token1, token2: Atom("name", E1, token1 + " " + token2),
        },
    ]
