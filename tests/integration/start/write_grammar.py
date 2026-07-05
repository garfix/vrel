from vrel.core.constants import E1
from vrel.entity.Atom import Atom
from vrel.entity.Variable import Variable

Name = Variable("Name")


def get_write_grammar():
    return [
        # sentences
        {
            "syn": "s() -> np(E1)",
            "if": [Atom("output_type", "list"), Atom("output_list", E1)],
            "list_element": E1,
            "list_combine": lambda nps: ", ".join(nps),
        },
        {
            "syn": "s() -> 'See you later!'",
            "if": [Atom("output_type", "close_conversation")],
        },
        # noun phrases
        {"syn": "np(E1) -> literal(Name)", "if": [Atom("name", E1, Name)]},
        {"syn": "np(E1) -> literal(E1)"},
    ]
