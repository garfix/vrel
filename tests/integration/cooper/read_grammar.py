from vrel.core.constants import E1, E2, E3, E4, E5
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable


T1 = Variable("T1")
T2 = Variable("T2")
T3 = Variable("T3")


def get_read_grammar():
    # I distinguish between
    # * proper nouns: instances of things, whose names are learned
    # * np's: complex statements about things that are available in the system
    # * common nouns/adj: the head of a induction rule can't be a complex np, but it can be a common noun
    # * usually proper nouns are parts of np's, but in this case this seems impossible

    return [
        # sentence
        # magnesium burns rapidly
        {
            "syn": "s() -> proper_noun(E1) vp(E1, T1)",
            "sem": lambda proper_noun, vp: [Atom("intent_tell", [proper_noun, vp], T1)],
        },
        # magnesium is a metal
        {
            "syn": "s() -> proper_noun(E1) 'is' np(E1, T1)",
            "sem": lambda proper_noun, np: [Atom("intent_tell", [proper_noun, np], T1)],
        },
        # gasoline is combustable
        {
            "syn": "s() -> proper_noun(E1) 'is' adj(E1, T1)",
            "sem": lambda proper_noun, adj: [Atom("intent_tell", [proper_noun, adj], T1)],
        },
        # X is Y
        {
            "syn": "s() -> proper_noun(E1) 'is' proper_noun(E2)",
            "sem": lambda proper_noun1, proper_noun2: [
                Atom("intent_tell", [Atom("same_as", proper_noun1, proper_noun2)], T1)
            ],
        },
        # mutual exclusivity
        # -A :- B
        # -B :- A
        # works only with facts are stored positively
        # cannot use A :- not(B), B :- not(A), because of infinite recursion
        {
            "syn": "s() -> common_noun(E1, T1) copula() 'not' common_noun(E2, T2)",
            "sem": lambda common_noun1, copula, common_noun2: [
                Atom(
                    "scoped2",
                    [
                        Atom("let", T1, "false"),
                        Atom("let", T2, "true"),
                        Atom("intent_learn", common_noun1, [common_noun2]),
                    ],
                ),
                Atom(
                    "scoped2",
                    [
                        Atom("let", T2, "false"),
                        Atom("let", T1, "true"),
                        Atom("intent_learn", common_noun2, [common_noun1]),
                    ],
                ),
            ],
        },
        # oxides are compounds
        {
            "syn": "s() -> common_noun(E1, T1) 'are' common_noun(E2, T2)",
            "sem": lambda common_noun1, common_noun2: [
                Atom("let", T1, "true"),
                Atom("let", T2, "true"),
                Atom("intent_learn", common_noun2, [common_noun1]),
            ],
        },
        # metals are metallic
        {
            "syn": "s() -> np(E1, T1) 'are' adj(E2, T2)",
            "sem": lambda common_noun, adj: [
                Atom("let", T1, "true"),
                Atom("let", T2, "true"),
                Atom("intent_learn", adj, [common_noun]),
            ],
        },
        # dark-gray things are not white
        # {
        #     "syn": "s() -> np(E1, T1) 'are' 'not' adj(E2, T2)",
        #     "sem": lambda np, adj: [
        #         Atom("let", T2, "false"),
        #         Atom("let", T1, "true"),
        #         Atom("intent_learn", adj, [np]),
        #     ],
        # },
        # no metal is a nonmetal
        {
            "syn": "s() -> 'no' common_noun(E1, T1) 'is' 'a' common_noun(E2, T2)",
            "sem": lambda common_noun1, common_noun2: [
                Atom("let", T2, "false"),
                Atom("let", T1, "true"),
                Atom("intent_learn", common_noun2, [common_noun1]),
            ],
        },
        # np
        {"syn": "np(E1, T1) -> a() nbar(E1, T1)", "sem": lambda a, nbar: nbar},
        {"syn": "np(E1, T1) -> nbar(E1, T1)", "sem": lambda nbar: nbar},
        {"syn": "np(E1, T1) -> 'not' np(E1, T2)", "sem": lambda np: Atom("not_3v", T2, T1).pre([np])},
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
            "sem": lambda adj, thing: adj,
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
        # adjective
        {"syn": "adj(E1, T1) -> 'white'", "sem": lambda: Atom("white", E1, T1)},
        {"syn": "adj(E1, T1) -> 'metallic'", "sem": lambda: Atom("metallic", E1, T1)},
        {"syn": "adj(E1, T1) -> 'dark-gray'", "sem": lambda: Atom("dark_gray", E1, T1)},
        {"syn": "adj(E1, T1) -> 'combustable'", "sem": lambda: Atom("combustable", E1, T1)},
        {"syn": "adj(E1, T1) -> 'brittle'", "sem": lambda: Atom("brittle", E1, T1)},
        {"syn": "adj(E1, T1) -> 'not' adj(E1, T2)", "sem": lambda adj: Atom("not_3v", T2, T1).pre([adj])},
        # common noun
        {"syn": "common_noun(E1, T1) -> 'compound'", "sem": lambda: Atom("compound", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'element'", "sem": lambda: Atom("element", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'metal'", "sem": lambda: Atom("metal", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'nonmetal'", "sem": lambda: Atom("nonmetal", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'oxide'", "sem": lambda: Atom("oxide", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'solid'", "sem": lambda: Atom("solid", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'gas'", "sem": lambda: Atom("gas", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'fuel'", "sem": lambda: Atom("fuel", E1, T1)},
        {
            "syn": "common_noun(E1, T1) -> common_noun(E1, T1)+'s'",
            "sem": lambda common_noun: common_noun,
        },
        # special
        {"syn": "thing() -> 'things'", "sem": lambda: None},
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
