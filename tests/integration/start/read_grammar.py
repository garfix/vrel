from vrel.core.constants import CONSTANT, E1, E2, E3, E4, COMBINED, SEPARATE
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

Age = Variable("Size")


def get_read_grammar():
    return [
        # sentence
        {
            # Example: Who is the oldest employee?
            "syn": "s(E1) -> 'who' 'is' np(E1) + '?'",
            "sem": lambda np: Atom("intent_single_name", [np]),
        },
        {
            # Bye
            "syn": "s(E1) -> 'bye'",
            "sem": lambda: Atom(
                "intent_close_conversation",
            ),
        },
        # np
        {
            "syn": "np(E1) -> aggregate(E1)",
            "sem": lambda aggregate: aggregate,
        },
        # aggregates
        {
            "syn": "aggregate(E1) -> 'the' 'oldest' nbar(E1)",
            "sem": lambda nbar: Atom("arg_max", E1, Age, [nbar], [Atom("age", E1, Age)]),
        },
        # nbar
        {
            "syn": "nbar(E1) -> noun(E1)",
            "sem": lambda noun: noun,
        },
        # noun
        {"syn": "noun(E1) -> 'employee'", "sem": lambda: Atom("employee", E1)},
    ]
