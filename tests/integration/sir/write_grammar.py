from vrel.core.constants import E1, E2
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

List1 = Variable("List")


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> 'I understand'",
            "if": [Atom("last_output", "understand")],
        },
        {
            "syn": "s() -> 'Insufficient information'",
            "if": [Atom("last_output", "unknown")],
        },
        {
            "syn": "s() -> 'No, they are the same'",
            "if": [Atom("last_output", "no_same")],
        },
        {
            "syn": "s() -> 'No, part means proper subpart'",
            "if": [Atom("last_output", "no_subpart")],
        },
        {
            "syn": "s() -> 'No, but the reverse is sometimes true'",
            "if": [Atom("last_output", "reverse_sometimes")],
        },
        {
            "syn": "s() -> 'Sometimes'",
            "if": [Atom("last_output", "sometimes")],
        },
        {
            "syn": "s() -> 'Yes'",
            "if": [Atom("last_output", "yes")],
        },
        {
            "syn": "s() -> 'No'",
            "if": [Atom("last_output", "no")],
        },
        {
            "syn": "s() -> 'The above statement is impossible'",
            "if": [Atom("last_output", "impossible")],
        },
        {
            "syn": "s() -> 'The answer is' literal(E1)",
            "if": [Atom("last_output", "count", E1)],
        },
        {
            "syn": "s() -> 'How many' thing(E1) 'per' thing(E2)+'?'",
            "if": [Atom("last_output", "how_many", E1, E2)],
        },
        {
            "syn": "s() -> 'Don\\'t know whether' thing(E1) 'is part of' thing(E2)",
            "if": [
                Atom("last_output", "dont_know_part_of", E1, E2),
            ],
        },
        {"syn": "s() -> custom()", "post": lambda custom: custom.strip()},
        # location
        {
            "syn": "custom() -> just_left_of(E1)? just_right_of(E1)? left_of(E1)? right_of(E1)?",
            "if": [Atom("last_output", "location", E1)],
        },
        {
            "syn": "just_left_of(E1) -> 'Just to the left of the' thing(E2)+'.'",
            "if": [Atom("just_left_of", E1, E2)],
        },
        {
            "syn": "just_right_of(E1) -> 'Just to the right of the' thing(E2)+'.'",
            "if": [Atom("just_left_of", E2, E1)],
        },
        {
            "syn": "right_of(E1) -> 'Somewhere to the right of the following ..' things(List)",
            "if": [
                Atom("find_all", E2, [Atom("somewhere_left_of", E2, E1)], List1),
                Atom("not", [Atom("equals", List1, [])]),
            ],
        },
        {
            "syn": "left_of(E1) -> 'Somewhere to the left of the following ..' things(List)",
            "if": [
                Atom("find_all", E2, [Atom("somewhere_left_of", E1, E2)], List1),
                Atom("not", [Atom("equals", List1, [])]),
            ],
        },
        # things
        {"syn": "thing(E1) -> format(E1)", "format": lambda thing: thing.id},
        {"syn": "things(E1) -> format(E1)", "format": lambda things: format_list(things)},
        # position
        # position_description is a predicate in SIRModule
        {
            "syn": "custom() -> 'The left-to-right order is as follows:' literal(E1)",
            "if": [Atom("last_output", "position"), Atom("position_description", E1)],
        },
    ]


def format_list(elements):
    flattened = [element.id for element in elements]
    return "(" + ", ".join(flattened) + ")"
