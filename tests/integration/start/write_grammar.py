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
            "per-element": True,
            "format": lambda elements: ", ".join(elements),
        },
        # ...
        {"syn": "np(E1) -> text(Name)", "if": [Atom("name", E1, Name)]},
        {
            "syn": "s() -> 'See you later!'",
            "if": [Atom("output_type", "close_conversation")],
        },
    ]
