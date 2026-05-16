from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

List1 = Variable("List")


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'I understand'",
            "if": [Atom("output_type", "understand")],
        },
        {
            "syn": "s() -> 'Insufficient information'",
            "if": [Atom("output_type", "unknown")],
        },
        {
            "syn": "s() -> 'No, they are the same'",
            "if": [Atom("output_type", "no_same")],
        },
        {
            "syn": "s() -> 'No, part means proper subpart'",
            "if": [Atom("output_type", "no_subpart")],
        },
        {
            "syn": "s() -> 'No, but the reverse is sometimes true'",
            "if": [Atom("output_type", "reverse_sometimes")],
        },
        {
            "syn": "s() -> 'Sometimes'",
            "if": [Atom("output_type", "sometimes")],
        },
        {
            "syn": "s() -> 'Yes'",
            "if": [Atom("output_type", "yes")],
        },
        {
            "syn": "s() -> 'No'",
            "if": [Atom("output_type", "no")],
        },
        {
            "syn": "s() -> 'The above statement is impossible'",
            "if": [Atom("output_type", "impossible")],
        },
        {
            "syn": "s() -> 'The answer is' text(E1)",
            "if": [Atom("output_type", "count"), Atom("output_count", E1)],
        },
        {
            "syn": "s() -> 'How many' text(E1) 'per' text(E2)+'?'",
            "if": [Atom("output_type", "how_many"), Atom("output_how_many", E1, E2)],
        },
        {
            "syn": "s() -> 'Don\\'t know whether' text(E1) 'is part of' text(E2)",
            "if": [
                Atom("output_type", "dont_know_part_of"),
                Atom("output_dont_know_part_of", E1, E2),
            ],
        },
        {"syn": "s() -> custom()", "post": lambda out: out.strip()},
        # location
        {
            "syn": "custom() -> just_left_of(E1)? just_right_of(E1)? left_of(E1)? right_of(E1)?",
            "if": [Atom("output_type", "location"), Atom("output_location", E1)],
        },
        {
            "syn": "just_left_of(E1) -> 'Just to the left of the' text(E2)+'.'",
            "if": [Atom("just_left_of", E1, E2)],
        },
        {
            "syn": "just_right_of(E1) -> 'Just to the right of the' text(E2)+'.'",
            "if": [Atom("just_left_of", E2, E1)],
        },
        {
            "syn": "right_of(E1) -> 'Somewhere to the right of the following ..' format(List)",
            "if": [
                Atom("find_all", E2, [Atom("somewhere_left_of", E2, E1)], List1),
                Atom("not", [Atom("equals", List1, [])]),
            ],
            "format": lambda elements: format_list(elements),
        },
        {
            "syn": "left_of(E1) -> 'Somewhere to the left of the following ..' format(List)",
            "if": [
                Atom("find_all", E2, [Atom("somewhere_left_of", E1, E2)], List1),
                Atom("not", [Atom("equals", List1, [])]),
            ],
            "format": lambda elements: format_list(elements),
        },
        # position
        # position_description is a predicate in SIRModule
        {
            "syn": "custom() -> 'The left-to-right order is as follows:' text(E1)",
            "if": [Atom("output_type", "position"), Atom("position_description", E1)],
        },
    ]


def format_list(elements):
    return "(" + ", ".join(elements) + ")"
