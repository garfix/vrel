from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom


def get_read_grammar():
    return [
        # sentences
        {
            "syn": "s() -> statement()",
            "sem": lambda statement: statement,
        },
        {
            "syn": "s() -> yes_no()",
            "sem": lambda yes_no: yes_no,
        },
        # statements
        # every X is a Y, where X and Y not part of the grammar
        # this is uncommon, is defines a new concept in terms of an another unknown concept
        {
            "syn": "statement() -> 'every' common_noun_name() 'is' a() common_noun_name()",
            "sem": lambda common_noun_name1, a, common_noun_name2: Atom(
                "intent_claim", [Atom("isa", common_noun_name1, common_noun_name2)]
            ),
        },
        # any X is an example of a Y
        {
            "syn": "statement() -> 'any' common_noun_name() 'is' 'an' 'example' 'of' a() common_noun_name()",
            "sem": lambda common_noun_name1, a, common_noun_name2: Atom(
                "intent_claim", [Atom("isa", common_noun_name1, common_noun_name2)]
            ),
        },
        # An IBM-7094 is a computer
        {
            "syn": "statement() -> a() common_noun_name() 'is' a() common_noun_name()",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: Atom(
                "intent_teach", [Atom("isa", common_noun_name1, common_noun_name2)]
            ),
        },
        # A finger is a part of a hand
        # a statement about classes as entities
        {
            "syn": "statement() -> a() common_noun_name() 'is' 'a'? 'part' 'of' a() common_noun_name()",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: Atom(
                "intent_teach", [Atom("part_of", common_noun_name1, common_noun_name2)]
            ),
        },
        # A screen is part of every display-device
        {
            "syn": "statement() -> a() common_noun_name() 'is' 'a'? 'part' 'of' 'every' common_noun_name()",
            "sem": lambda a1, common_noun_name1, common_noun_name2: Atom(
                "intent_teach", [Atom("part_of", common_noun_name1, common_noun_name2)]
            ),
        },
        # A van-dyke is part of Ferren
        {
            "syn": "statement() -> a() common_noun_name() 'is' 'a'? 'part' 'of' proper_noun(E1)",
            "sem": lambda a1, common_noun_name, proper_noun: Atom(
                "intent_teach", [Atom("part_of", common_noun_name, proper_noun)]
            ),
        },
        # There are two hands on each person
        # a statement about classes as quantified entities
        {
            "syn": "statement() -> 'there' 'are' number(E1) common_noun_name() 'on' 'each' common_noun_name()",
            "sem": lambda number, common_noun_name1, common_noun_name2: Atom(
                "intent_teach",
                [
                    Atom("part_of", common_noun_name1, common_noun_name2),
                    Atom("part_of_n", common_noun_name1, common_noun_name2, number),
                ],
            ),
        },
        # John is a boy
        # Max is an IBM-7094
        # Jack is a dope
        {
            "syn": "statement() -> proper_noun(E1) 'is' a() common_noun_name()",
            "sem": lambda proper_noun, a2, common_noun_name: Atom(
                "intent_teach", [Atom("isa", proper_noun, common_noun_name)]
            ),
        },
        # Every hand has 5 fingers
        {
            "syn": "statement() -> 'every' common_noun_name() 'has' number(E1) common_noun_name()",
            "sem": lambda common_noun_name1, number, common_noun_name2: [
                (
                    "intent_teach",
                    [
                        ("part_of", common_noun_name2, common_noun_name1),
                        ("part_of_n", common_noun_name2, common_noun_name1, number),
                    ],
                )
            ],
        },
        # Tom has nine fingers
        # Dick has one hand
        {
            "syn": "statement() -> proper_noun(E1) 'has' number(E1) common_noun_name()",
            "sem": lambda proper_noun, number, common_noun_name: proper_noun
            + [
                (
                    "intent_teach",
                    [
                        ("part_of", common_noun_name, E1),
                        ("part_of_n", common_noun_name, E1, number),
                    ],
                )
            ],
        },
        # John is Jack
        {
            "syn": "statement() -> proper_noun(E1) 'is' proper_noun(E2)",
            "sem": lambda proper_noun1, proper_noun2: Atom(
                "intent_teach", [Atom("identical", proper_noun1, proper_noun2)]
            ),
        },
        # Every fireman owns a pair-of-red-suspenders
        {
            "syn": "statement() -> 'every' common_noun_name() own() a() common_noun_name()",
            "sem": lambda common_noun_name1, own, a, common_noun_name2: Atom(
                "intent_teach", [Atom("own", common_noun_name1, common_noun_name2)]
            ),
        },
        # Alfred owns a log-log-decitrig
        {
            "syn": "statement() -> proper_noun(E1) own() a() common_noun_name()",
            "sem": lambda proper_noun, own, a, common_noun_name: Atom(
                "intent_teach", [Atom("own", proper_noun, common_noun_name)]
            ),
        },
        # The telephone is just to the right of the book
        {
            "syn": "s(E3) -> proper_noun(E1) 'is' preposition(E1, E2) proper_noun(E2)",
            "sem": lambda proper_noun1, preposition, proper_noun2: proper_noun1
            + proper_noun2
            + [("intent_claim", preposition)],
        },
        # questions
        # How many fingers does John have?
        # we don't know John, but all that matters is that it's a boy
        # determine 'how many' not by counting but by calculating
        {
            "syn": "s() -> 'how' 'many' common_noun(E1) 'does' proper_noun(E2) 'have'+'?'",
            "sem": lambda common_noun1, proper_noun: common_noun1
            + proper_noun
            + [("intent_count", [("have", E2, E1)])],
        },
        # Is a X a Y?
        {
            "syn": "s() -> 'is' a() common_noun_name() a() common_noun_name()~'?'",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: Atom(
                "intent_isa", common_noun_name1, common_noun_name2
            ),
        },
        # Is a nostril part of a professor?
        # Is a nostril part of a living-creature?
        # Is a living-creature part of a nose?
        {
            "syn": "s() -> 'is' a() common_noun_name() 'a'? 'part' 'of' a() common_noun_name()~'?'",
            "sem": lambda a1, common_noun_name1, a2, common_noun_name2: Atom(
                "intent_part_of", common_noun_name1, common_noun_name2
            ),
        },
        # Is a beard part of Ferren?
        {
            "syn": "s() -> 'is' a() common_noun_name() 'a'? 'part' 'of' proper_noun(E2)~'?'",
            "sem": lambda a1, common_noun_name, proper_noun: Atom("intent_part_of", common_noun_name, proper_noun),
        },
        # Yes/no questions
        # Is Max a computer?
        # Is John a dope?
        {
            "syn": "s() -> 'is' proper_noun(E1) a() common_noun_name()~'?'",
            "sem": lambda proper_noun, a, common_noun_name: Atom("intent_isa", proper_noun, common_noun_name),
        },
        # Does Alfred own a slide-rule?
        {
            "syn": "yes_no() -> 'does' proper_noun(E1) own() a() common_noun_name()~'?'",
            "sem": lambda proper_noun, own, a, common_noun_name: Atom("intent_own", proper_noun, common_noun_name),
        },
        # Does a doctor own a pair-of-red-suspenders?
        # Does a firechief own a pair-of-red-suspenders?
        # Does an engineering-student own a log-log-decitrig?
        # Does a pair-of-red-suspenders own a pair-of-red-suspenders?
        {
            "syn": "s() -> 'does' a() common_noun_name() own() a() common_noun_name()~'?'",
            "sem": lambda a1, common_noun_name1, own, a2, common_noun_name2: Atom(
                "intent_some_own", common_noun_name1, common_noun_name2
            ),
        },
        # Is the pad just to the right of the book?
        {
            "syn": "s() -> 'is' proper_noun(E1) preposition(E1, E2) proper_noun(E2)~'?'",
            "sem": lambda proper_noun1, preposition, proper_noun2: [
                (
                    "with_context",
                    "question",
                    [("intent_yn", proper_noun1 + proper_noun2 + preposition)],
                )
            ],
        },
        # Where is the pad?
        {
            "syn": "s() -> 'where' 'is' proper_noun(E1)~'?'",
            "sem": lambda proper_noun: [("intent_where", e1, proper_noun)],
        },
        # What is the position of the pad?
        {
            "syn": "s() -> 'what' 'is' 'the' 'position' 'of' proper_noun(E1)~'?'",
            "sem": lambda proper_noun: [("intent_position",)],
        },
        # number
        {"syn": "number(E1) -> 'one'", "sem": lambda: 1},
        {"syn": "number(E1) -> 'two'", "sem": lambda: 2},
        {"syn": "number(E1) -> 'nine'", "sem": lambda: 9},
        {"syn": "number(E1) -> '5'", "sem": lambda: 5},
        # article
        {"syn": "a() -> 'a'", "sem": lambda: []},
        {"syn": "a() -> 'an'", "sem": lambda: []},
        # verb
        {"syn": "own() -> 'own'", "sem": lambda: []},
        {"syn": "own() -> 'owns'", "sem": lambda: []},
        # common noun
        {
            "syn": "common_noun(E1) -> common_noun_name()",
            "sem": lambda common_noun_name: [(common_noun_name, E1)],
        },
        # preposition
        {
            "syn": "preposition(E1, E2) -> 'just' 'to' 'the' 'left' 'of'",
            "sem": lambda: [("just_left_of", E1, E2)],
        },
        {
            "syn": "preposition(E1, E2) -> 'just' 'to' 'the' 'right' 'of'",
            "sem": lambda: [("just_left_of", E2, E1)],
        },
        {
            "syn": "preposition(E1, E2) -> 'to' 'the' 'left' 'of'",
            "sem": lambda: [("left_of", E1, E2)],
        },
        {
            "syn": "preposition(E1, E2) -> 'to' 'the' 'right' 'of'",
            "sem": lambda: [("left_of", E2, E1)],
        },
        # proper noun
        {
            "syn": "proper_noun(E1) -> 'the'? name()",
            "sem": lambda name: Atom("name", E1, name),
        },
        # introduction of a new common noun
        {"syn": "common_noun_name() -> name()", "sem": lambda name: name},
        {
            "syn": "common_noun_name() -> common_noun_name()+'s'",
            "sem": lambda common_noun_name: common_noun_name,
            "boost": 1,
        },
        {"syn": "name() -> /\\w[\\w\\d]+(-[\\w\\d]+)*/", "sem": lambda token: token},
    ]
