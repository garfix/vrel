from vrel.core.constants import E1, E2, E3, E4, E5
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

T1 = Variable("T1")
T2 = Variable("T2")
T3 = Variable("T3")
T4 = Variable("T4")
Name = Variable("name")


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
        # salt is natrium chloride
        # magnesium is magnesium
        {
            "syn": "s() -> proper_noun(E1) 'is' proper_noun(E2)",
            "sem": lambda proper_noun1, proper_noun2: [
                Atom(
                    "intent_tell",
                    # on query, use `same_as` query function: provide nonempty resultset on success
                    # on write, simply write to the table `same_as`
                    [Atom("same_as", proper_noun1, proper_noun2), Atom("let", T1, "true")],
                    T1,
                )
            ],
        },
        # elements are not compounds
        # mutual exclusivity
        # -A :- B
        # -B :- A
        # works only with facts are stored positively
        # cannot use A :- not(B), B :- not(A), because of infinite recursion
        {
            "syn": "s() -> common_noun(E1, T1) copula() 'not' common_noun(E1, T2)",
            "sem": lambda common_noun1, copula, common_noun2: [
                Atom(
                    "scope",
                    [
                        Atom("intent_learn", [common_noun1], [common_noun2], T1, T2, "false", "true"),
                    ],
                ),
                Atom(
                    "scope",
                    [
                        Atom("intent_learn", [common_noun2], [common_noun1], T2, T1, "false", "true"),
                    ],
                ),
            ],
        },
        # oxides are compounds, compound(X) :- oxide(X)
        {
            "syn": "s() -> np(E1, T1) 'are' common_noun(E2, T2)",
            "sem": lambda common_noun1, common_noun2: [
                Atom("intent_learn", [common_noun2], [common_noun1], T2, T1, "true", "true"),
            ],
        },
        # metals are metallic, metallic(X) :- metal(X)
        # oxides are not white
        # dark-gray things are not white
        {
            "syn": "s() -> np(E1, T1) 'are' adj(E1, T2)",
            "sem": lambda np, adj: [
                Atom("intent_learn", [adj], [np], T2, T1, "true", "true"),
            ],
        },
        # some oxides are white
        {
            "syn": "s() -> 'some' nbar(E1, T2) 'are' adj(E1, T3)",
            "sem": lambda np, adj: [
                Atom("intent_check", [Atom("and_3v", [np], [adj], T2, T3, T1)], T1),
            ],
        },
        # every oxide is an oxide
        {
            "syn": "s() -> 'every' common_noun(E1, T1) 'is' a() common_noun(E1, T2)",
            "sem": lambda common_noun1, a, common_noun2: [
                Atom("intent_learn", [common_noun2], [common_noun1], T2, T1, "true", "true"),
            ],
        },
        # anything that is not a compound is not ferrous sulfide
        {
            "syn": "s() -> 'anything' 'that' 'is' 'not' 'a' common_noun(E1, T2) 'is' not_proper_noun(E1, T3)",
            "sem": lambda np, not_proper_noun: [
                Atom(
                    "intent_check", [Atom("let", T2, "false"), Atom("and_3v", [np], [not_proper_noun], T2, T3, T1)], T1
                ),
            ],
        },
        # no oxide is white
        {
            "syn": "s() -> 'no' np(E1, T2) 'is' adj(E1, T3)",
            "sem": lambda np, adj: [
                Atom(
                    "intent_check",
                    [
                        Atom(
                            "not_3v",
                            [Atom("and_3v", [np], [adj], T2, T3, T1)],
                            T1,
                            T4,
                        )
                    ],
                    T4,
                ),
            ],
        },
        # no metal is a nonmetal
        # no dark-gray thing is a sulfide
        {
            "syn": "s() -> 'no' np(E1, T1) 'is' 'a' common_noun(E1, T2)",
            "sem": lambda common_noun1, common_noun2: [
                Atom(
                    "intent_learn",
                    [Atom("not_3v", [common_noun2], T2, T4)],
                    [common_noun1],
                    T4,
                    T1,
                    "true",
                    "true",
                ),
            ],
        },
        # a solid is not a gas
        {
            "syn": "s() -> a() common_noun(E1, T1) 'is' 'not' 'a' common_noun(E1, T2)",
            "sem": lambda a, common_noun1, common_noun2: [
                Atom("intent_learn", [common_noun2], [common_noun1], T2, T1, "false", "true"),
            ],
        },
        # any thing that burns rapidly burns
        {
            "syn": "s() -> 'any' nbar(E1, T1) vp(E1, T2)",
            "sem": lambda nbar, vp: [
                Atom("intent_learn", [vp], [nbar], T2, T1, "true", "true"),
            ],
        },
        # combustable things burn
        {
            "syn": "s() -> np(E1, T1) vp(E1, T2)",
            "sem": lambda nbar, vp: [
                Atom("intent_learn", [vp], [nbar], T2, T1, "true", "true"),
            ],
        },
        # np
        {"syn": "np(E1, T1) -> a() nbar(E1, T1)", "sem": lambda a, nbar: nbar},
        {"syn": "np(E1, T1) -> nbar(E1, T1)", "sem": lambda nbar: nbar},
        {"syn": "np(E1, T1) -> 'not' np(E1, T2)", "sem": lambda np: Atom("not_3v", [np], T2, T1)},
        # nbar
        {"syn": "nbar(E1, T1) -> noun(E1, T1)", "sem": lambda noun: noun},
        {
            "syn": "nbar(E1, T1) -> nbar(E1, T2) 'that' vp(E1, T3)",
            "sem": lambda nbar, vp: Atom("and_3v", [nbar], [vp], T2, T3, T1),
        },
        {
            "syn": "nbar(E1, T1) -> thing() 'that' vp(E1, T1)",
            "sem": lambda thing, vp: vp,
        },
        {
            "syn": "nbar(E1, T1) -> adj(E1, T2) nbar(E1, T3)",
            "sem": lambda adj, nbar: Atom("and_3v", [adj], [nbar], T2, T3, T1),
        },
        {
            "syn": "nbar(E1, T1) -> adj(E1, T1) thing()",
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
        {"syn": "adj(E1, T1) -> 'not' adj(E1, T2)", "sem": lambda adj: Atom("not_3v", [adj], T2, T1)},
        # common noun
        {"syn": "common_noun(E1, T1) -> 'compound'", "sem": lambda: Atom("compound", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'element'", "sem": lambda: Atom("element", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'metal'", "sem": lambda: Atom("metal", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'nonmetal'", "sem": lambda: Atom("nonmetal", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'oxide'", "sem": lambda: Atom("oxide", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'sulfide'", "sem": lambda: Atom("sulfide", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'solid'", "sem": lambda: Atom("solid", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'gas'", "sem": lambda: Atom("gas", E1, T1)},
        {"syn": "common_noun(E1, T1) -> 'fuel'", "sem": lambda: Atom("fuel", E1, T1)},
        {
            "syn": "common_noun(E1, T1) -> common_noun(E1, T1)+'s'",
            "sem": lambda common_noun: common_noun,
        },
        # special
        {"syn": "thing() -> 'thing'", "sem": lambda: None},
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
        {
            "syn": "proper_noun(E1) -> /\\w+/ common_noun(E1, T1)",
            "sem": lambda token, common_noun: Atom("name", E1, token + " " + common_noun.predicate).execute(
                [Atom("let", T1, "true"), Atom("store", [common_noun])]
            ),
        },
        {
            "syn": "not_proper_noun(E1, T1) -> 'not' proper_noun(E2)",
            "sem": lambda proper_noun: Atom(
                "not_equals_3v",
                E1,
                proper_noun,
                T1,
            ),
        },
    ]
